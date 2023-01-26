"""
Packet Similarity.
"""
from scipy.spatial.distance import hamming


class ComparePackets:
    """
    An object that compares packets given a specific configuration.
    """

    def __init__(self, decay=0.85):
        self.decay = decay

    def distance(self, p1, p2):
        """
        Compute the distance between two packets.
        """
        res = (False, 0)

        # We assert that xfer_type, endpoint and setup must be the same,
        # before considering anything else.
        if p1.xfer_type != p2.xfer_type:
            return res

        print('> endpoint', p1.endpoint, p2.endpoint)
        if p1.endpoint != p2.endpoint:
            return res

        # Validate the setup, allow non-matching setup lengths

        print('> bmRequestType',
              p1.setup.bmRequestType(),
              p2.setup.bmRequestType()
              )

        if p1.setup.bmRequestType() != p2.setup.bmRequestType():
            return res

        if p1.setup.bRequest() != p2.setup.bRequest():
            return res

        if p1.setup.wValue() != p2.setup.wValue():
            return res

        if p1.setup.wIndex() != p2.setup.wIndex():
            return res

        print('made it')

        if len(p1.payload) == 0:
            return (True, 0)

        if len(p1.payload) != len(p2.payload):
            return res

        print('hit')

        # now go through each byte in data, earlier bytes are more meaninful
        # for distance than later bytes.
        weights = [self.decay ** i for i in range(len(p1.payload))]
        dist = hamming(list(p1.payload), list(p2.payload), weights)

        return (True, dist)
