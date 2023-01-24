from device.basedevice import BaseDevice
from device.strings import Strings
from device.descriptors import FixedDescriptor, MaxSize
from analysis.analysis import PCAPAnalysis
from analysis.similarity import ComparePackets, ComparablePacket


class EmulatedDevice(BaseDevice):
    """
    Emulate a device from packet captures.
    """

    def __init__(self, pcaps):
        # We need the following:
        # * device descriptor, so we can display info
        # * configuration descriptors
        # * string descriptors.
        analysis = PCAPAnalysis(pcaps)
        self.analysis = analysis
        self._configurations = analysis.configuration()

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

    def message_handler(self, packet):
        """
        Return an approiate packet in response.
        """
        if packet.setup == b'\x00' * 8:
            return None

        p1 = ComparablePacket(
                0,
                packet.ep,
                len(packet.transfer_buffer),
                packet.setup,
                packet.transfer_buffer
            )
        cp = ComparePackets()

        def score_function(pair):
            if pair['C'] is None or pair['S'] is None:
                return (False, 0)

            ps = pair['S']
            p2 = ComparablePacket(
                0,
                ps.epnum,
                len(bytes(ps.payload)),
                bytes(ps.setup),
                bytes(ps.payload)
            )
            return cp.distance(p1, p2)

        res = self.analysis.search(score_function)

        # nothing close, just return nothing
        if len(res) == 0:
            return MaxSize(None, 0)

        return FixedDescriptor(bytes(res[0][1]['C'].payload))
