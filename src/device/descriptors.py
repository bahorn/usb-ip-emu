"""
Classes implementing various USB descriptors.
"""
import struct
import copy

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
    def __init__(self, data, max_length=None):
        # self.configurations = configurations
        data_fixed = copy.deepcopy(data)

        # Compute the max size, in case this needs bLength
        bLength = sum(i for i, _ in self.ORDER)
        if 'bLength' not in data_fixed:
            data_fixed['bLength'] = bLength

        if max_length and data_fixed['bLength'] > max_length:
            data_fixed['bLength'] = max_length

        if 'bDescriptorType' not in data_fixed:
            data_fixed['bDescriptorType'] = self.TYPE.value

        self.data = data_fixed
        self.max_length = max_length

    def pack(self):
        message = b''
        for size, key in self.ORDER:
            match size:
                case 1:
                    message += struct.pack('<B', self.data[key])
                case 2:
                    message += struct.pack('<H', self.data[key])

        if self.max_length:
            message = message[:self.max_length]

        return message


class DeviceDescriptor(BaseDescriptor):
    TYPE = DescriptorTypes.DEVICE

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
        (1, 'iProduct'),
        (1, 'iSerialNumber'),
        (1, 'bNumConfigurations')
    ]


class ConfigurationDescriptor(BaseDescriptor):
    TYPE = DescriptorTypes.CONFIGURATION

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


class String0Descriptor(BaseDescriptor):
    """
    String descriptor at index 0 returns a list of all the supported languages.
    """
    TYPE = DescriptorTypes.STRING

    def __init__(self, languages, max_length=None):
        self.languages = languages
        self.max_length = max_length

    def pack(self):
        message = b''
        length = 2 + 2 * len(self.languages)

        message += struct.pack('<B', length)
        message += struct.pack('<B', DescriptorTypes.STRING.value)

        for language_code in self.languages:
            message += struct.pack('<H', language_code)

        if self.max_length:
            return message[:self.max_length]

        return message


class StringDescriptor(BaseDescriptor):
    TYPE = DescriptorTypes.STRING

    def __init__(self, string, max_length=None):
        self.string = string
        self.max_length = max_length

    def pack(self):
        string = self.string.encode('utf-16')[2:]
        length = len(string) + 2
        if self.max_length and self.max_length < length:
            length = self.max_length

        message = b''
        message += struct.pack('<B', length)
        message += struct.pack('<B', DescriptorTypes.STRING.value)
        message += string

        if self.max_length:
            return message[:self.max_length]

        return message


class InterfaceDescriptor(BaseDescriptor):
    TYPE = DescriptorTypes.INTERFACE

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


class EndpointDescriptor(BaseDescriptor):
    TYPE = DescriptorTypes.ENDPOINT

    ORDER = [
        (1, 'bLength'),
        (1, 'bDescriptorType'),
        (1, 'bEndpointAddress'),
        (1, 'bmAttributes'),
        (2, 'wMaxPacketSize'),
        (1, 'bInterval')
    ]
