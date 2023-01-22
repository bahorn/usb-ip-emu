from enum import Enum


class Recipient(Enum):
    DEVICE = 0
    INTERFACE = 1
    ENDPOINT = 2
    OTHER = 3


class Type(Enum):
    STANDARD = 0
    CLASS = 1
    VENDOR = 2
    RESERVED = 3


class TransferDirection(Enum):
    HOST_TO_DEVICE = 0
    DEVICE_TO_HOST = 1


class FeatureSelector:
    ENDPOINT_HALT = 0
    DEVICE_REMOTE_WAKEUP = 1
    TEST_MODE = 2
    B_HNP_ENABLE = 3
    A_HNP_SUPPORT = 4
    A_ALT_HNP_SUPPORT = 5
