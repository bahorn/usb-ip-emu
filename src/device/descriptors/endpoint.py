from .base import BaseDescriptor
from protocol.usb.enum import DescriptorTypes


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
