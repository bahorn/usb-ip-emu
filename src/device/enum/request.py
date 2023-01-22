from enum import Enum

class StandardRequestID(Enum):
    # https://www.beyondlogic.org/usbnutshell/usb6.shtml
    GET_STATUS = 0x00
    CLEAR_FEATURE = 0x01
    SET_FEATURE = 0x03
    SET_ADDRESS = 0x05
    GET_DESCRIPTOR = 0x06
    SET_DESCRIPTOR = 0x07
    GET_CONFIGURATION = 0x08
    SET_CONFIGURATION = 0x09

    GET_INTERFACE = 0x0a
    SET_INTERFACE = 0x11

    SYNCH_FRAME = 0x12
