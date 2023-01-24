"""
Packet Similarity.
"""
from scipy.spatial.distance import hamming


class ComparablePacket:
    """
    Unified representing of a USB packet, to allow comparison from different
    sources.
    """

    def __init__(self, xfer_type, endpoint, length, setup, payload):
        self.data = {
            'xfer_type': xfer_type,
            'endpoint': endpoint,
            'length': length,
            'setup': setup,
            'payload': payload
        }


class ComparePackets:
    """
    An object that compares packets given a specific configuration.
    """

    def __init__(self, decay=0.85):
        self.decay = decay

    def distance(self, packet1, packet2):
        """
        Compute the distance between two packets.
        """
        p1 = packet1.data
        p2 = packet2.data

        res = (False, 0)

        # We assert that xfer_type, endpoint and setup must be the same,
        # before considering anything else.
        if p1['xfer_type'] != p2['xfer_type']:
            return res

        if p1['endpoint'] != p2['endpoint']:
            return res

        if p1['setup'] != p2['setup']:
            return res

        if p1['length'] != p2['length']:
            return res

        if len(p1['payload']) != len(p2['payload']):
            return res

        if len(p1['payload']) == 0:
            return (True, 0)

        print('hit')
        # now go through each byte in data, earlier bytes are more meaninful
        # for distance than later bytes.
        weights = [self.decay ** i for i in range(len(p1['payload']))]
        dist = hamming(list(p1['payload']), list(p2['payload']), weights)

        return (True, dist)
