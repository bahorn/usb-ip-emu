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

    def __init__(self, setting):
        if isinstance(setting, list):
            self.languages = {language: {} for language in setting}
        else:
            self.languages = setting

    def set_strings(self, language, strings):
        """
        Update the strings stored for a language.
        """
        active = {}
        if isinstance(active, list):
            for idx, string in enumerate(strings):
                active[idx + 1] = string
        else:
            active = strings

        self.languages[language] = active

    def descriptor(self, index, language):
        """
        Return a descriptor for the given string
        """
        if index == 0 and language == 0:
            # just return the String0Descriptor
            return String0Descriptor(self.languages.keys())

        if index not in self.languages[language]:
            return StringDescriptor('Unknown')

        return StringDescriptor(self.languages[language][index])
