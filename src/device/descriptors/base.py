"""
Classes implementing various USB descriptors.
"""
import struct
import copy


class BaseDescriptor:
    def __init__(self, data):
        data_fixed = copy.deepcopy(data)

        # Compute the max size, in case this needs bLength
        bLength = sum(i for i, _ in self.ORDER)
        if 'bLength' not in data_fixed:
            data_fixed['bLength'] = bLength

        if 'bDescriptorType' not in data_fixed:
            data_fixed['bDescriptorType'] = self.TYPE.value

        self.data = data_fixed

    def pack(self, max_length=None):
        if max_length and self.data['bLength'] > max_length:
            self.data['bLength'] = max_length

        message = b''
        for size, key in self.ORDER:
            match size:
                case 1:
                    message += struct.pack('<B', self.data[key])
                case 2:
                    message += struct.pack('<H', self.data[key])

        if max_length:
            message = message[:max_length]

        return message
