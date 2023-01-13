"""
Exceptions
"""


class ParseError(Exception):
    """
    Usable Error format for the message processing.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'ParseError: {self.message}'


class VersionError(Exception):
    """
    Version unknown error
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'VersionError: {self.message}'
