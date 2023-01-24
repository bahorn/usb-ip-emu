from .usbmon import USBmon, SetupPacket, StringDescriptor, DeviceDescriptor
from scapy.all import rdpcap


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
            for packet in capture:
                pkt = USBmon(bytes(packet))
                if pkt.id not in pairs:
                    pairs[pkt.id] = {'S': None, 'C': None}
                pairs[pkt.id][chr(pkt.type)] = pkt
        return pairs

    def match(self, func):
        """
        Return a request and response if the request satifies `func`
        """
        result = []
        current = [None, None]
        for capture in self.pcaps:
            for packet in capture:
                pkt = USBmon(bytes(packet))
                if current[0]:
                    # add the reply to the pair
                    if pkt.id == current[0].id:
                        current[1] = pkt

                    result.append(current)
                    current = [None, None]

                if func(pkt):
                    current = [pkt, None]

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
            if 'setup' not in pkt.fields:
                return False
            setup = SetupPacket(pkt.setup)
            if 'descriptor_type' not in setup.fields:
                return False
            return setup.descriptor_type == 0x01 and \
                setup.descriptor_index == 0x00

        for request, response in self.ps.match(is_device):
            setup = SetupPacket(request.setup)

            if setup.wLength >= device_descriptor[0]:
                device_descriptor = (
                        setup.wLength,
                        DeviceDescriptor(bytes(response.payload)).fields
                    )
        return device_descriptor

    def configuration(self):
        """
        Dumping configuration descriptors.
        """
        configurations = {}

        # search for any packets that contain a GET DESCRIPTOR message.
        def is_configuration(pkt):
            if 'setup' not in pkt.fields:
                return False
            setup = SetupPacket(pkt.setup)
            if 'descriptor_type' not in setup.fields:
                return False
            return setup.descriptor_type == 0x02

        for request, response in self.ps.match(is_configuration):
            setup = SetupPacket(request.setup)
            if setup.descriptor_index not in configurations:
                configurations[setup.descriptor_index] = (0, None)

            # check if this is requesting more than we've previously seen.
            if setup.wLength <= configurations[setup.descriptor_index][0]:
                continue

            configurations[setup.descriptor_index] = \
                (setup.wLength, bytes(response.payload))

        return configurations

    def strings(self):
        """
        Dumping string descriptors.
        """
        # American English will exist in pretty much every device.
        strings = {}

        def is_string(pkt):
            if 'setup' not in pkt.fields:
                return False

            setup = SetupPacket(pkt.setup)

            if 'descriptor_type' not in setup.fields:
                return False

            return setup.descriptor_type == 0x03 and \
                setup.descriptor_index != 0x00

        # find packets that contain string information.
        for request, response in self.ps.match(is_string):
            setup = SetupPacket(request.setup)
            language_id = setup.wIndex
            string_idx = setup.descriptor_index
            length = setup.wLength
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

    def search(self, func):
        return self.ps.score(func)