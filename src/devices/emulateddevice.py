from device.basedevice import BaseDevice
from device.strings import Strings
from device.descriptors import FixedDescriptor, MaxSize
from analysis.analysis import PCAPAnalysis
from analysis.similarity import ComparePackets


class EmulatedDevice(BaseDevice):
    """
    Emulate a device from packet captures.
    """

    def __init__(self, pcaps, callbacks=None):
        # We need the following:
        # * device descriptor, so we can display info
        # * configuration descriptors
        # * string descriptors.
        self.callbacks = callbacks
        analysis = PCAPAnalysis(pcaps)
        self.analysis = analysis
        self._configurations = analysis.configuration()
        self._hid_reports = analysis.hid_reports()

        strings = analysis.strings()
        self._strings = Strings(strings)

        config = analysis.device()[1]
        self.VID = config['idVendor']
        self.PID = config['idProduct']

        super().__init__(config)

        self._active_configuration = 1

    def configuration(self, configuration_idx):
        raw_descriptor = self._configurations[configuration_idx][1]
        return [FixedDescriptor(raw_descriptor)]

    def hid_report(self, setup):
        raw_descriptor = self._hid_reports.get(
            (setup.interface_number(), setup.descriptor_index()),
            None
        )
        if raw_descriptor:
            return [FixedDescriptor(raw_descriptor[1])]

        return None

    def pre_response(self, packet):
        """
        Function that is called when recieving a packet.

        For logging and correcting the packet.
        """
        self.callback('pre_response', (packet, ))
        return packet

    def post_response(self, packet, response):
        """
        Function that is called on response.

        Allows things like logging, etc.
        """
        self.callback('post_response', (packet, response))
        return response

    def recommendation(self, packet):
        """
        Return an approiate packet in response.
        """
        print(packet.setup)
        if packet.setup.bytes == b'\x00' * 8:
            return None

        p1 = packet
        cp = ComparePackets()

        def score_function(pair):
            if pair['S'] is None:
                return (False, 0)

            p2 = pair['S']
            return cp.distance(p1, p2)

        res = self.analysis.search(score_function)

        # for these, we need to consider the wLength() value.

        self.callback('recommendation', (packet, res))

        # nothing close, just return nothing
        if len(res) == 0:
            return MaxSize(None, 0)

        best = res[0]

        if not best[1]['C']:
            return None
        print(best[1]['C'])

        return FixedDescriptor(bytes(best[1]['C'].payload))

    def message_handler(self, packet):
        """
        Return an approiate packet in response.
        """
        return self.recommendation(packet)

    def callback(self, name, args):
        """
        Callbacks so outside code can hook into this and print / display
        information.
        """
        if not self.callbacks or name not in self.callbacks:
            return

        self.callbacks[name](*args)
