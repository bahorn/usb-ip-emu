"""
Endpoint
"""
from bitarray import bitarray

from .descriptors import EndpointDescriptor
from .enum import TransferType, SynchronisationType, UsageType


class Endpoint:
    def __init__(self, address, max_packet_size, interval,
                 transfer_type=TransferType.CONTROL,
                 synchronisation_type=SynchronisationType.NO_SYNCHRONISATION,
                 usage_type=UsageType.DATA_ENDPOINT):

        self._address = address
        self._max_packet_size = max_packet_size
        self._interval = interval
        self._transfer_type = transfer_type
        self._synchronisation_type = synchronisation_type
        self._usage_type = usage_type

    def attributes(self):
        resp = bitarray()

        # this might need fixing when actually implementing ISO transfers.
        resp += [0, 0]
        resp += self._usage_type.value
        resp += self._synchronisation_type.value
        resp += self._transfer_type.value

        return resp

    def descriptor(self):
        """
        Return an endpoint descriptor for this endpoint.
        """

        return EndpointDescriptor(
            {
                'bEndpointAddress': self._address,
                'bmAttributes': int.from_bytes(self.attributes(), 'little'),
                'wMaxPacketSize': self._max_packet_size,
                'bInterval': self._interval
            }
        )
