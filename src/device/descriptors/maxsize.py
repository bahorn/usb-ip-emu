from .base import BaseDescriptor


class MaxSize(BaseDescriptor):
    """
    Wrapper around a descriptor, so that pack() doesn't require an argument.
    """

    def __init__(self, descriptor, max_size):
        self.descriptor = descriptor
        self.max_size = max_size

    def pack(self):
        res = b''
        if not self.descriptor:
            return res

        if isinstance(self.descriptor, BaseDescriptor):
            return self.descriptor.pack(self.max_size)

        if isinstance(self.descriptor, list):
            for descriptor in self.descriptor:
                res += descriptor.pack()

            if self.max_size:
                res = res[:self.max_size]

        return res
