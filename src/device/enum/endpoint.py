from enum import Enum

class TransferType(Enum):
    CONTROL = (0, 0)
    ISOCHRONOUS = (0, 1)
    BULK = (1, 0)
    INTERUPT = (1, 1)


class SynchronisationType(Enum):
    NO_SYNCHRONISATION = (0, 0)
    ASYNCHRONOUS = (0, 1)
    ADAPTIVE = (1, 0)
    SYNCHRONOUS = (1, 1)


class UsageType(Enum):
    DATA_ENDPOINT = (0, 0)
    FEEDBACK_ENDPOINT = (0, 1)
    IMPLICIT_FEEDBACK_DATA_ENDPOINT = (1, 0)
    RESERVED = (1, 1)
