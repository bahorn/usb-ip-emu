import struct

from .base import BaseDescriptor
from device.enum import DescriptorTypes


class String0Descriptor(BaseDescriptor):
    """
    String descriptor at index 0 returns a list of all the supported languages.
    """
    TYPE = DescriptorTypes.STRING

    def __init__(self, languages):
        self.languages = languages

    def pack(self, max_length=None):
        message = b''
        length = 2 + 2 * len(self.languages)

        message += struct.pack('<B', length)
        message += struct.pack('<B', DescriptorTypes.STRING.value)

        for language_code in self.languages:
            message += struct.pack('<H', language_code)

        if max_length:
            return message[:max_length]

        return message


class StringDescriptor(BaseDescriptor):
    TYPE = DescriptorTypes.STRING

    def __init__(self, string):
        self.string = string

    def pack(self, max_length=None):
        string = self.string.encode('utf-16')[2:]
        length = len(string) + 2
        if max_length and max_length < length:
            length = self.max_length

        message = b''
        message += struct.pack('<B', length)
        message += struct.pack('<B', DescriptorTypes.STRING.value)
        message += string

        if max_length:
            return message[:max_length]

        return message
