"""
Endpoint
"""
from bitarray import bitarray
from enum import Enum

from .descriptors import EndpointDescriptor


class TransferType(Enum):
    CONTROL = (0, 0)
    ISOCHRONOUS = (0, 1)
    BULK = (1, 0)
    INTERUPT = (1, 1)


class SynchronisationType(Enum):
    NO_SYNCHRONISATION = (0, 0)
    ASYNCHRONOUS = (0, 1)
    ADAPTIVE = (1, 0)
    SYNCHRONOUS = (1, 1)


class UsageType(Enum):
    DATA_ENDPOINT = (0, 0)
    FEEDBACK_ENDPOINT = (0, 1)
    IMPLICIT_FEEDBACK_DATA_ENDPOINT = (1, 0)
    RESERVED = (1, 1)


class Endpoint:
    def __init__(self, address, max_packet_size, interval, transfer_type,
                 synchronisation_type, usage_type):
        self._address = address
        self._max_packet_size = max_packet_size
        self._interval = interval
        self._transfer_type = transfer_type
        self._synchronisation_type = synchronisation_type
        self._usage_type = usage_type

    def attributes(self):
        resp = bitarray()

        resp.append(self._transfer_type.value)
        resp.append(self._synchronisation_type.value)
        resp.append(self._usage_type.value)
        resp.append([0, 0])

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
