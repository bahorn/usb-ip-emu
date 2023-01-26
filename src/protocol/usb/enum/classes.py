"""
Defined USB classes
"""
from enum import Enum


class ClassCodes(Enum):
    """
    From:
    https://www.usb.org/defined-class-codes
    """

    UNSPECIFIED = 0x00
    AUDIO = 0x01
    COMMUNICATIONS = 0x02
    HID = 0x03
    PID = 0x05
    MEDIA = 0x06
    PRINTER = 0x07
    MASS_STORAGE = 0x08
    HUB = 0x09
    DATA = 0x0a
    SMART_CARD = 0x0b
    CONTENT_SECURITY = 0x0d
    VIDEO = 0x0e
    PHDC = 0x0f
    AV = 0x10
    BILLBOARD = 0x11
    DIAGNOSTIC = 0xdc
    WIRELESS_CONTROLLER = 0xe0
    MISCELLANEOUS = 0xef
    APPLICATION_SPECIFIC = 0xfe
    VENDOR_SPECIFIC = 0xff
