from protocol.usbmon import \
        USBmon, \
        SetupPacket, \
        StringDescriptor, \
        DeviceDescriptor
import random
from protocol.usb.enum import DescriptorTypes
from protocol.usb.setup import DeviceGetDescriptor, HIDReport
from protocol.usb import USBPacket
from scapy.all import rdpcap, Raw
from scapy.layers.usb import USBpcap, USBpcapTransferControl


class PacketSearch:
    """
    Implementation of various packet searching functions.
    """

    def __init__(self, files):
        self.pcaps = [rdpcap(file) for file in files]
        self._pairs = self.pairs()

    def pairs(self):
        """
        Convert a set of captures into pairs.
        """
        pairs = {}
        for capture in self.pcaps:
            i = random.randint(0, 10000)
            for packet in capture:
                to_skip, id, type, new_pkt = True, None, None, None

                # need to handle usbmon / usbpcap differently.
                if isinstance(packet, USBpcap):
                    to_skip, id, type, new_pkt = self.usbpcap(packet)
                else:
                    to_skip, id, type, new_pkt = self.usbmon(packet)

                if to_skip:
                    continue

                key = f'{i}_{id}'
                if key not in pairs:
                    pairs[key] = {'S': None, 'C': None}

                pairs[key][type] = new_pkt

        return pairs

    def usbpcap(self, packet):
        # Don't need to do any conversion, as it is already a usbpcap.
        id = packet.irpId

        if USBpcapTransferControl not in packet:
            return True, None, None, None

        status = packet[USBpcapTransferControl].stage
        # setup / complete
        stage = {0: 'S', 3: 'C'}.get(status)

        setup = b'\x00'*8
        payload = b''

        match stage:
            case 'S':
                body = bytes(packet[Raw])
                setup = body[:8]
                payload = body[8:]
            case 'C':
                if Raw in packet:
                    payload = bytes(packet[Raw])

        new_pkt = USBPacket(
            0,
            packet.endpoint,
            setup,
            payload
        )

        return False, id, stage, new_pkt

    def usbmon(self, packet):
        pkt = USBmon(bytes(packet))
        id = pkt.id

        new_pkt = USBPacket(
            0,
            pkt.epnum,
            pkt.setup,
            bytes(pkt.payload)
        )

        return False, id, chr(pkt.type), new_pkt

    def match(self, func):
        """
        Return a request and response if the request satifies `func`
        """
        result = []

        for _, pair in self._pairs.items():
            if not pair['S']:
                continue

            if func(pair['S']):
                result.append([pair['S'], pair['C']])

        return result

    def score(self, func):
        scores = []
        for _, pair in self._pairs.items():
            add, score = func(pair)
            if not add:
                continue

            scores.append((score, pair))

        scores.sort(key=lambda x: x[0])
        return scores


class PCAPAnalysis:
    """
    Find and dump useful information in a USB pcap
    """

    def __init__(self, files):
        self.ps = PacketSearch(files)

    def device(self):
        """
        Dumping the device descriptor
        """
        device_descriptor = (0, None)

        def is_device(pkt):
            setup = pkt.setup
            if not isinstance(setup, DeviceGetDescriptor):
                return False

            return setup.descriptor_type() == DescriptorTypes.DEVICE and \
                setup.descriptor_index() == 0x00

        for request, response in self.ps.match(is_device):
            setup = request.setup
            print(response.payload)

            if setup.wLength() >= device_descriptor[0]:
                device_descriptor = (
                        setup.wLength(),
                        DeviceDescriptor(bytes(response.payload)).fields
                    )

        print(device_descriptor)
        return device_descriptor

    def configuration(self):
        """
        Dumping configuration descriptors.
        """
        configurations = {}

        # search for any packets that contain a GET DESCRIPTOR message.
        def is_configuration(pkt):
            setup = pkt.setup
            if not isinstance(setup, DeviceGetDescriptor):
                return False

            return setup.descriptor_type() == DescriptorTypes.CONFIGURATION

        for request, response in self.ps.match(is_configuration):
            setup = request.setup

            if setup.descriptor_index() not in configurations:
                configurations[setup.descriptor_index()] = (0, None)

            # check if this is requesting more than we've previously seen.
            if setup.wLength() <= configurations[setup.descriptor_index()][0]:
                continue

            configurations[setup.descriptor_index()] = \
                (setup.wLength(), bytes(response.payload))

        return configurations

    def strings(self):
        """
        Dumping string descriptors.
        """
        # American English will exist in pretty much every device.
        strings = {}

        def is_string(pkt):
            setup = pkt.setup
            if not isinstance(setup, DeviceGetDescriptor):
                return False

            return setup.descriptor_type() == DescriptorTypes.STRING and \
                setup.descriptor_index() != 0x00

        # find packets that contain string information.
        for request, response in self.ps.match(is_string):
            setup = request.setup
            language_id = setup.wIndex()
            string_idx = setup.descriptor_index()
            length = setup.wLength()
            descriptor = StringDescriptor(bytes(response.payload))
            string = bytes(descriptor.payload).decode('utf-16')

            if language_id not in strings:
                strings[language_id] = {}

            if string_idx in strings[language_id]:
                # need to verify if its longer or not.
                if strings[language_id][string_idx][0] > length:
                    continue

            strings[language_id][string_idx] = (length, string)

        return strings

    def hid_reports(self):
        """
        Dump the GET_DESCRIPTOR hid report
        """
        hid_reports = {}

        def is_hid_report(pkt):
            setup = pkt.setup
            if not isinstance(setup, HIDReport):
                return False

            return setup.descriptor_type() == DescriptorTypes.REPORT and \
                setup.bmRequestType() != 0x81

        for request, response in self.ps.match(is_hid_report):
            setup = request.setup
            descriptor_index = setup.descriptor_index()
            interface_number = setup.wIndex()
            key = (interface_number, descriptor_index)
            if key not in hid_reports:
                hid_reports[key] = (0, None)

            if setup.wLength() <= hid_reports[key][0]:
                continue

            hid_reports[key] = (setup.wLength(), bytes(response.payload))

        return hid_reports

    def search(self, func):
        return self.ps.score(func)
