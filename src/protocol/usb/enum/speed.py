from enum import Enum


class USBSpeed(Enum):
    """
    Speed IDs.
    Obtained from the indices in speed_strings[] from the linux kernel
    """
    UNKNOWN = 0
    LOW_SPEED = 1
    FULL_SPEED = 2
    HIGH_SPEED = 3
    WIRELESS = 4
    SUPER_SPEED = 5
