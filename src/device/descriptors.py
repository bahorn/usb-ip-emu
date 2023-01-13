"""
Classes implementing various USB descriptors.
"""
import struct

from enum import Enum


class USBVersions:
    """
    BCD Representation of USB versions.
    """
    USB_3_0 = 0x0300
    USB_3_1 = 0x0310
    USB_3_2 = 0x0320
    USB_2_0 = 0x0200
    USB_1_1 = 0x0110
    USB_1_0 = 0x0100


class DescriptorTypes(Enum):
    DEVICE = 0x01
    CONFIGURATION = 0x02
    STRING = 0x03
    INTERFACE = 0x04
    ENDPOINT = 0x05


class BaseDescriptor:
    def __init__(self):
        self.data = {}

    def pack(self):
        message = b''
        for size, key in self.ORDER:
            match size:
                case 1:
                    message += struct.pack('>B', self.data[key])
                case 2:
                    message += struct.pack('>H', self.data[key])

        return message


class DeviceDescriptor(BaseDescriptor):
    ORDER = [
        (1, 'bLength'),
        (1, 'bDescriptorType'),
        (2, 'bcdUSB'),
        (1, 'bDeviceClass'),
        (1, 'bDeviceSubClass'),
        (1, 'bDeviceProtocol'),
        (1, 'bMaxPacketSize'),
        (2, 'idVendor'),
        (2, 'idProduct'),
        (2, 'bcdDevice'),
        (1, 'iManufacturer'),
        (1, 'iSerialNumber'),
        (1, 'bNumConfigurations')
    ]

    def __init__(self, data, configurations):
        self.configurations = configurations
        super().__init__()


class ConfigurationDescriptor(BaseDescriptor):
    ORDER = [
        (1, 'bLength'),
        (1, 'bDescriptorType'),
        (2, 'wTotalLength'),
        (1, 'bNumInterfaces'),
        (1, 'bConfigurationValue'),
        (1, 'iConfiguration'),
        (1, 'bmAttributes'),
        (1, 'bMaxPower')
    ]

    def __init__(self, interfaces):
        self.interfaces = interfaces
        super().__init__()

    def pack(self):
        message = b''

        return message


class String0Descriptor(BaseDescriptor):
    """
    String descriptor at index 0 returns a list of all the supported languages.
    """

    def __init__(self, languages):
        self.languages = []
        super().__init__()

    def pack(self):
        message = b''
        length = 0

        message += struct.pack('>B', length)
        message += struct.pack('>B', DescriptorTypes.STRING.value)
        for language_code in self.languages:
            message += struct.pack('>H', language_code)
        return message


class StringDescriptor(BaseDescriptor):
    def __init__(self, string):
        super().__init__()
        self.string = string

    def pack(self):
        message = b''
        message += struct.pack('>B', len(self.string))
        message += struct.pack('>B', DescriptorTypes.STRING.value)
        message += bytes(self.string, 'ascii')
        return message


class InterfaceDescriptor(BaseDescriptor):
    ORDER = [
        (1, 'bLength'),
        (1, 'bDescriptorType'),
        (1, 'bInterfaceNumber'),
        (1, 'bAlternateSetting'),
        (1, 'bNumEndpoints'),
        (1, 'bInterfaceClass'),
        (1, 'bInterfaceSubClass'),
        (1, 'bInterfaceProtocol'),
        (1, 'iInterface')
    ]

    def __init__(self, endpoints):
        self.endpoints = []
        super().__init__()

    def pack(self):
        message = super().pack()
        for endpoint in self.endpoints:
            message += EndpointDescriptor(endpoint).pack()
        return message


class EndpointDescriptor(BaseDescriptor):
    ORDER = [
        (1, 'bLength'),
        (1, 'bDescriptorType'),
        (1, 'bEndpointAddress'),
        (1, 'bmAttributes'),
        (2, 'wMaxPacketSize'),
        (1, 'bInterval')
    ]

    def __init__(self, data):
        self.data = data
        self.data['bLength'] = 7
        self.data['bDescriptorType'] = DescriptorTypes.ENDPOINT.value
        # device needs to define the res.
        super().__init__()
