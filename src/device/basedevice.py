"""
Base device to inherit from.
"""
from enum import Enum


class StandardRequestID(Enum):
    # https://www.beyondlogic.org/usbnutshell/usb6.shtml
    GET_STATUS = 0x00
    CLEAR_FEATURE = 0x01
    SET_FEATURE = 0x03
    SET_ADDRESS = 0x05
    GET_DESCRIPTOR = 0x06
    SET_DESCRIPTOR = 0x07
    GET_CONFIGURATION = 0x08
    SET_CONFIGURATION = 0x09

    GET_INTERFACE = 0x0a
    SET_INTERFACE = 0x11

    SYNCH_FRAME = 0x12


class BaseDevice:
    """
    Base class to implement more advanced devices on top of.

    It takes a dictionary for each of the settings.
    """

    def __init__(self, settings, interfaces):
        self.settings = settings
        self._interfaces = interfaces

    def busnum(self):
        return self.settings['busnum']

    def devnum(self):
        return self.settings['devnum']

    def speed(self):
        return self.settings['speed']

    def idVendor(self):
        return self.settings['idVendor']

    def idProduct(self):
        return self.settings['idProduct']

    def bcdDevice(self):
        return self.settings['bcdDevice']

    def bDeviceClass(self):
        return self.settings['bDeviceClass']

    def bDeviceSubClass(self):
        return self.settings['bDeviceSubClass']

    def bDeviceProtocol(self):
        return self.settings['bDeviceProtocol']

    def bConfigurationValue(self):
        return self.settings['bConfigurationValue']

    def bNumConfigurations(self):
        return self.settings['bNumConfigurations']

    def bNumInterfaces(self):
        return len(self._interfaces)

    def interfaces(self):
        return self._interfaces

    def command(self, data):
        """
        Function that is called on each command.
        """
        pass

    # Implementations of standard requests.

    # GET_STATUS
    def get_status(self):
        pass

    # CLEAR_FEATURE
    def clear_feature(self):
        pass

    # SET_FEATURE
    def set_feature(self):
        pass

    # SET_ADDRESS
    def set_address(self):
        pass

    # GET_DESCRIPTOR
    def get_discriptor(self):
        pass

    # SET_DESCRIPTOR
    def set_descriptor(self):
        pass

    # GET_CONFIGURATION
    def get_configuration(self):
        pass

    # SET_CONFIGURATION
    def set_configuration(self):
        pass
