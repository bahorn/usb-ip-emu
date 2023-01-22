from .base import BaseDescriptor
from device.enum import DescriptorTypes

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
