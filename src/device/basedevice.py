"""
Base device to inherit from.
"""
from .descriptors import \
        DeviceDescriptor, \
        DescriptorTypes, \
        MaxSize

from protocol.usb.setup import \
        DeviceGetStatus, \
        DeviceClearFeature, \
        DeviceSetFeature, \
        DeviceSetAddress, \
        DeviceGetDescriptor, \
        DeviceSetDescriptor, \
        DeviceGetConfiguration, \
        DeviceSetConfiguration, \
        HIDReport, \
        SetIdle

from protocol.usb.enum import USBVersions
from protocol.usb.enum import USBSpeed


class BaseDevice:
    """
    Base class to implement more advanced devices on top of.

    It takes a dictionary for each of the settings.
    """
    _configurations = []
    _strings = []
    _active_configuration = 0
    _interfaces = []

    def __init__(self, settings):
        self.settings = settings

        if 'bConfigurationValue' in self.settings:
            self._active_configuration = self.settings['bConfigurationValue']

    def speed(self):
        return USBSpeed.HIGH_SPEED.value

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
        return self.settings.get(
                'bConfigurationValue',
                self._active_configuration
            )

    def bNumConfigurations(self):
        return self.settings.get(
                'bNumConfigurations', len(self._configurations)
            )

    def bcdUSB(self):
        return self.settings.get('bcdUSB', USBVersions.USB_2_0.value)

    def bMaxPacketSize(self):
        return self.settings.get('bMaxPacketSize', 64)

    def bNumInterfaces(self):
        return len(self._interfaces)

    def iManufacturer(self):
        return self.settings.get('iManufacturer', 0)

    def iProduct(self):
        return self.settings.get('iProduct', 0)

    def iSerialNumber(self):
        return self.settings.get('iSerialNumber', 0)

    def interfaces(self):
        return self._interfaces

    def max_power_consumption(self):
        return self.settings.get('bMaxPower', 100)

    def command(self, packet):
        """
        Process an URB for this device.
        """
        packet_ = self.pre_response(packet)
        setup = packet_.setup

        result = None
        handled = True
        no_reply = False

        match setup:
            # Default Device Requests
            case _ if isinstance(setup, DeviceGetStatus):
                result = self.get_status(setup)
            case _ if isinstance(setup, DeviceClearFeature):
                result = self.clear_feature(setup)
            case _ if isinstance(setup, DeviceSetFeature):
                result = self.set_feature(setup)
            case _ if isinstance(setup, DeviceSetAddress):
                result = self.set_address(setup)
            case _ if isinstance(setup, DeviceGetDescriptor):
                result = self.get_discriptor(setup)
            case _ if isinstance(setup, DeviceSetDescriptor):
                result = self.set_descriptor(setup)
            case _ if isinstance(setup, DeviceGetConfiguration):
                result = self.get_configuration(setup)
            case _ if isinstance(setup, DeviceSetConfiguration):
                result = self.set_configuration(setup)
            case _ if isinstance(setup, HIDReport):
                result = self.hid_report(setup)
            case _ if isinstance(setup, SetIdle):
                self.set_idle(setup)
                no_reply = True
            case _:
                handled = False

        if no_reply:
            return None

        if handled:
            return MaxSize(result, setup.wLength())

        return self.message_handler(packet_)

    def descriptor(self):
        return DeviceDescriptor(
            {
                'bcdUSB': self.bcdUSB(),
                'bDeviceClass': self.bDeviceClass(),
                'bDeviceSubClass': self.bDeviceSubClass(),
                'bDeviceProtocol': self.bDeviceProtocol(),
                'bMaxPacketSize': self.bMaxPacketSize(),
                'idVendor': self.idVendor(),
                'idProduct': self.idProduct(),
                'bcdDevice': self.bcdDevice(),
                'iManufacturer': self.iManufacturer(),
                'iProduct': self.iProduct(),
                'iSerialNumber': self.iSerialNumber(),
                'bNumConfigurations': self.bNumConfigurations()
            }
        )

    def configuration(self, configuration_idx):
        return self._configurations[configuration_idx].descriptor()

    def strings(self, string_idx, language):
        return self._strings.descriptor(string_idx, language)

    # Implementations of standard device requests.

    # GET_STATUS
    def get_status(self, setup):
        """
        Not implemented yet
        """
        return None

    # CLEAR_FEATURE
    def clear_feature(self, setup):
        """
        Not implemented yet
        """
        return None

    # SET_FEATURE
    def set_feature(self, setup):
        """
        Not implemented yet
        """
        return None

    # SET_ADDRESS
    def set_address(self, setup):
        """
        Not implemented yet
        """
        return None

    # GET_DESCRIPTOR
    def get_discriptor(self, setup):
        match setup.descriptor_type():
            case DescriptorTypes.DEVICE:
                return self.descriptor()
            case DescriptorTypes.CONFIGURATION:
                return self.configuration(
                            setup.descriptor_index()
                        )
            case DescriptorTypes.STRING:
                return self.strings(
                        setup.descriptor_index(),
                        setup.language_id()
                    )
            case DescriptorTypes.INTERFACE:
                # Not yet implemented
                return None
            case DescriptorTypes.ENDPOINT:
                # Not yet implemented
                return None

    # SET_DESCRIPTOR
    def set_descriptor(self, setup):
        """
        Not implemented yet
        """
        return None

    # GET_CONFIGURATION
    def get_configuration(self, setup):
        """
        Not implemented yet
        """
        return None

    # SET_CONFIGURATION
    def set_configuration(self, setup):
        self._active_configuration = setup.configuration_value()
        return None

    # HID REPORT request
    def hid_report(self, setup):
        return None

    # SET_IDLE
    def set_idle(self, setup):
        pass

    def unknown(self, setup):
        """
        Unknown setup command!
        """
        print('unknown setup command')
        return None

    def pre_response(self, packet):
        """
        Called when receiving a packet, allows modification of the packet or do
        implement logging, etc.
        """
        return packet

    def post_response(self, packet, response):
        """
        Called after deciding a response, allows modification to the response.
        """
        return response

    def message_handler(self, packet):
        """
        Unknown packet, clases inheriting from this should replace it with one
        that handles the specific device it is implementing.
        """
        return MaxSize(None, 0)
