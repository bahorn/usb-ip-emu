from .base import BaseDescriptor
from device.enum import DescriptorTypes


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


