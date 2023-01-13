"""
Interface related code
"""


class Interface:
    """
    Class representing an interface.
    """

    def __init__(self, if_class, if_subclass, if_protocol):
        self.if_class = if_class
        self.if_subclass = if_subclass
        self.if_protocol = if_protocol

    def bInterfaceClass(self):
        return self.if_class

    def bInterfaceSubClass(self):
        return self.if_subclass

    def bInterfaceProtocol(self):
        return self.if_protocol
