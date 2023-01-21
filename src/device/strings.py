"""
Manage the strings used by a device.
"""
from enum import Enum

from .descriptors import String0Descriptor, StringDescriptor


class Languages(Enum):
    """
    I am not copying pasting all of these.
    """
    ENGLISH_US = 0x0409


class Strings:
    """
    Manage the strings in a device.
    """

    def __init__(self, languages):
        self.languages = {language: [] for language in languages}

    def set_strings(self, language, strings):
        """
        Update the strings stored for a language.
        """
        self.languages[language] = strings

    def descriptor(self, index, language):
        """
        Return a descriptor for the given string
        """
        if index == 0 and language == 0:
            # just return the String0Descriptor
            return String0Descriptor(self.languages.keys())

        return StringDescriptor(self.languages[language][index - 1])
