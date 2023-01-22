from enum import Enum


class USBVersions(Enum):
    """
    BCD Representation of USB versions.
    """
    USB_3_0 = 0x0300
    USB_3_1 = 0x0310
    USB_3_2 = 0x0320
    USB_2_0 = 0x0200
    USB_1_1 = 0x0110
    USB_1_0 = 0x0100
