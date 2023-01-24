from .base import BaseDescriptor


class FixedDescriptor(BaseDescriptor):
    """
    Return a fixed set of bytes as the descriptor.

    Used to send descriptors that were previously logged.
    """

    def __init__(self, descriptor):
        self.descriptor = descriptor

    def pack(self):
        return self.descriptor
