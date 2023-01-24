import struct
from .enum import \
        Recipient, \
        Type, \
        TransferDirection, \
        StandardRequestID as Request
from .descriptors import DescriptorTypes


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

    def __init__(self, setup_data):
        bmRequestType, bRequest, wValue, wIndex, wLength \
                = struct.unpack('<BBHHH', setup_data)
        self._bmRequestType = bmRequestType
        self._bRequest = Request(bRequest)
        self._wValue = wValue
        self._wIndex = wIndex
        self._wLength = wLength

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

    def match(self, bmRequestType=None, bRequest=None, wValue=None,
              wIndex=None, wLength=None):
        """
        Check if the setup data and data matches.
        """
        if bmRequestType:
            if self.bmRequestType() != bmRequestType:
                return False

        if bRequest:
            if self.bRequest() != bRequest:
                return False

        if wValue:
            if self.wValue() != wValue:
                return False

        if wIndex:
            if self.wIndex() != wIndex:
                return False

        if wLength:
            if wLength != self.wLength():
                return False

        return True


# Standard Device Requests

class DeviceRequest(USBSetup):
    pass


class DeviceGetStatus(DeviceRequest):
    # Further data is sent during the data stage.
    pass


class DeviceClearFeature(DeviceRequest):
    def feature(self):
        return FeatureSelector(self.wValue())


class DeviceSetFeature(DeviceRequest):
    def feature(self):
        return FeatureSelector(self.wValue())


class DeviceSetAddress(DeviceRequest):
    def address(self):
        return self.wValue()


class DeviceGetDescriptor(DeviceRequest):
    def descriptor_type(self):
        return DescriptorTypes(
                    self.wValue().to_bytes(2, byteorder='little')[1]
                )

    def descriptor_index(self):
        return self.wValue().to_bytes(2, byteorder='little')[0]

    def language_id(self):
        return self.wIndex()

    def descriptor_length(self):
        return self.wLength()


class DeviceSetDescriptor(DeviceRequest):
    def language_id(self):
        return self.wIndex()

    def descriptor_length(self):
        return self.wLength()


class DeviceGetConfiguration(DeviceRequest):
    pass


class DeviceSetConfiguration(DeviceRequest):
    def configuration_value(self):
        return self.wValue()


# Standard Interface Requests

class InterfaceRequest(USBSetup):
    def __init__(self, setup_data):
        super().__init__(setup_data)

    def interface(self):
        # only 8 bits of this get used.
        return self.wIndex()


class InterfaceGetStatus(InterfaceRequest):
    pass


class InterfaceClearFeature(InterfaceRequest):
    pass


class InterfaceSetFeature(InterfaceRequest):
    pass


class InterfaceGetInterface(InterfaceRequest):
    pass


class InterfaceSetInterface(InterfaceRequest):
    pass


# Standard Endpoint Requests

class EndpointRequest(USBSetup):
    def __init__(self, setup_data):
        super().__init__(setup_data)

    def endpoint(self):
        field = self.wIndex()
        # D7 = direction
        # D0-D4 = endpoint number
        return field


class EndpointGetStatus(EndpointRequest):
    pass


class EndpointClearFeature(EndpointRequest):
    pass


class EndpointSetFeature(EndpointRequest):
    pass


class EndpointSynchFrame(EndpointRequest):
    pass


def process_USB_setup(setup_data):
    """
    Return the class representing the correct USB Setup request.
    """
    setup = USBSetup(setup_data)

    resp = setup

    # See if it matches a standard Message type, if so, return that instead.
    standard_packets = [
        # Standard Device Requests
        ((0b10000000, Request.GET_STATUS, 0, 0, 2), DeviceGetStatus),
        ((0b00000000, Request.CLEAR_FEATURE, None, 0, 0), DeviceClearFeature),
        ((0b00000000, Request.SET_FEATURE, None, 0, 0), DeviceSetFeature),
        ((0b00000000, Request.SET_ADDRESS, None, 0, 0), DeviceSetAddress),
        ((0b10000000, Request.GET_DESCRIPTOR, None, None, None),
            DeviceGetDescriptor),
        ((0b00000000, Request.SET_DESCRIPTOR, None, None, None),
            DeviceSetDescriptor),
        ((0b10000000, Request.GET_CONFIGURATION, 0, 0, 1),
            DeviceGetConfiguration),
        ((0b00000000, Request.SET_CONFIGURATION, None, 0, 0),
            DeviceSetConfiguration),
        # Standard Interface Requests
        ((0b10000001, Request.GET_STATUS, 0, None, 2), InterfaceGetStatus),
        ((0b00000001, Request.CLEAR_FEATURE, None, None, 0),
            InterfaceClearFeature),
        ((0b00000001, Request.SET_FEATURE, None, None, 0),
            InterfaceSetFeature),
        ((0b10000001, Request.GET_INTERFACE, 0, None, 1),
            InterfaceGetInterface),
        ((0b00000001, Request.SET_INTERFACE, None, None, 0),
            InterfaceSetInterface),
        # Standard Endpoint Requests
        ((0b10000010, Request.GET_STATUS, 0, None, 2), EndpointGetStatus),
        ((0b00000010, Request.CLEAR_FEATURE, None, None, 0),
            EndpointClearFeature),
        ((0b00000010, Request.SET_FEATURE, None, None, 0), EndpointSetFeature),
        ((0b10000010, Request.SYNCH_FRAME, 0, None, 2), EndpointSynchFrame)
    ]

    for standard_packet, type in standard_packets:
        if setup.match(standard_packet[0], standard_packet[1],
                       standard_packet[2], standard_packet[3],
                       standard_packet[4]):
            return type(setup_data)

    return resp
