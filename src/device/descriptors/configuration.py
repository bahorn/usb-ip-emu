from .base import BaseDescriptor
from protocol.usb.enum import DescriptorTypes


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
