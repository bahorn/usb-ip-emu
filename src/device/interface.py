"""
Interface related code
"""
from .descriptors import InterfaceDescriptor


class Interface:
    """
    Class representing an interface.
    """

    def __init__(self, interface_number, if_class=0x00, if_subclass=0x00,
                 if_protocol=0x00, alternate_setting=0, name_idx=0):
        self._interface_number = interface_number
        self._if_class = if_class
        self._if_subclass = if_subclass
        self._if_protocol = if_protocol
        self._alternate_setting = alternate_setting
        self._name_idx = name_idx
        self._endpoints = []

    def add_endpoints(self, endpoints):
        self._endpoints = endpoints

    def bInterfaceClass(self):
        return self.if_class

    def bInterfaceSubClass(self):
        return self.if_subclass

    def bInterfaceProtocol(self):
        return self.if_protocol

    def endpoints(self):
        return self._endpoints

    def descriptor(self):
        """
        Return a descriptor for this interface.
        """
        return InterfaceDescriptor(
            {
                'bInterfaceNumber': self._interface_number,
                'bAlternateSetting': self._alternate_setting,
                'bNumEndpoints': len(self._endpoints),
                'bInterfaceClass': self._if_class,
                'bInterfaceSubClass': self._if_subclass,
                'bInterfaceProtocol': self._if_protocol,
                'iInterface': self._name_idx
            }
        )
