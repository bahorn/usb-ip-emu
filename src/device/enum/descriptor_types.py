from enum import Enum

class DescriptorTypes(Enum):
    DEVICE = 0x01
    CONFIGURATION = 0x02
    STRING = 0x03
    INTERFACE = 0x04
    ENDPOINT = 0x05
    DEVICE_QUALIFIER = 0x06
    OTHER_SPEED_CONFIGURATION = 0x07
    INTERFACE_POWER = 0x08

    HID = 0x21
