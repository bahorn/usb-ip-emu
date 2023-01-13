import struct
from enum import Enum


class Recipient(Enum):
    DEVICE = 0
    INTERFACE = 1
    ENDPOINT = 2
    OTHER = 3


class Type(Enum):
    STANDARD = 0
    CLASS = 1
    VENDOR = 2
    RESERVED = 3


class TransferDirection(Enum):
    HOST_TO_DEVICE = 0
    DEVICE_TO_HOST = 1


class RequestType:
    def __init__(self, data):
        values = bin(data)[2:]
        self.recipient = Recipient(int(values[0:4][::-1], 2))
        self.type = Type(int(values[4:6][::-1], 2))
        self.transfer_direction = TransferDirection(int(values[7], 2))


class USBSetup:
    """
    Process a USBSetup message.
    
    Keeping it raw for now, so its easier to parse things later on.
    """

    def __init__(self, data):
        bmRequestType, bRequest, wValue, wIndex, wLength \
                = struct.unpack('>BBHHH', data)
        self._bmRequestType = bmRequestType
        self._bRequest = bRequest
        self._wValue = wValue
        self._wIndex = wIndex
        self._wLength = wLength

        print(self._bmRequestType, self._bRequest, self._wValue, self._wIndex,
                self._wLength)

    def bmRequestType(self):
        return self._bmRequestType

    def bRequest(self):
        return self._bRequest

    def wValue(self):
        return self._wValue

    def wIndex(self):
        return self._wIndex

    def wLength(self):
        return self._wLength
