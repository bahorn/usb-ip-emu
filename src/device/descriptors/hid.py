from .base import BaseDescriptor
from protocol.usb.enum import DescriptorTypes


class HIDDescriptor(BaseDescriptor):
    TYPE = DescriptorTypes.HID

    ORDER = [
        (1, 'bLength'),
        (1, 'bDescriptorType'),
        (2, 'bcdHID'),
        (1, 'bCountryCode'),
        (1, 'bNumDescriptors'),
        (1, 'bDescriptorType2'),
        (2, 'bDescriptorLength')
    ]
