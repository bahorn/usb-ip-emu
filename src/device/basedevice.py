"""
Base device to inherit from.
"""
from .configuration import Configuration
from .interface import Interface
from .strings import Strings, Languages
from .descriptors import \
        DeviceDescriptor, \
        DescriptorTypes, \
        USBVersions, \
        MaxSize
from .setup import \
        process_USB_setup, \
        DeviceGetStatus, \
        DeviceClearFeature, \
        DeviceSetFeature, \
        DeviceSetAddress, \
        DeviceGetDescriptor, \
        DeviceSetDescriptor, \
        DeviceGetConfiguration, \
        DeviceSetConfiguration


class BaseDevice:
    """
    Base class to implement more advanced devices on top of.

    It takes a dictionary for each of the settings.
    """

    def __init__(self, settings, interfaces):
        self.settings = settings
        self._interfaces = interfaces

        interface1 = Interface(0, name_idx=2)
        config1 = Configuration(1)
        config1.add_interface(interface1)

        self._configurations = [config1]
        self._strings = Strings([Languages.ENGLISH_US.value])
        self._strings.set_strings(
                Languages.ENGLISH_US.value, ['Hello world1', 'Hello world2']
            )

        self._active_configuration = 1

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

    def max_power_consumption(self):
        return self.settings.get('bMaxPower', 100)

    def command(self, packet):
        """
        Process an URB for this device.
        """
        setup = process_USB_setup(packet.setup)
        print(setup)

        result = None

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
            case _:
                print('unhandled message type!')

        return MaxSize(result, setup.wLength())

    def descriptor(self):
        return DeviceDescriptor(
            {
                'bcdUSB': USBVersions.USB_2_0,
                'bDeviceClass': self.bDeviceClass(),
                'bDeviceSubClass': self.bDeviceSubClass(),
                'bDeviceProtocol': self.bDeviceProtocol(),
                'bMaxPacketSize': 64,
                'idVendor': self.idVendor(),
                'idProduct': self.idProduct(),
                'bcdDevice': self.bcdDevice(),
                'iManufacturer': 1,
                'iProduct': 0,
                'iSerialNumber': 0,
                'bNumConfigurations': self.bNumConfigurations()
            }
        )

    def configuration(self, configuration_idx):
        return self._configurations[configuration_idx - 1].descriptor()

    def strings(self, string_idx, language):
        return self._strings.descriptor(string_idx, language)

    # Implementations of standard device requests.

    # GET_STATUS
    def get_status(self, setup):
        pass

    # CLEAR_FEATURE
    def clear_feature(self, setup):
        pass

    # SET_FEATURE
    def set_feature(self, setup):
        pass

    # SET_ADDRESS
    def set_address(self, setup):
        pass

    # GET_DESCRIPTOR
    def get_discriptor(self, setup):
        match setup.descriptor_type():
            case DescriptorTypes.DEVICE:
                return self.descriptor()
            case DescriptorTypes.CONFIGURATION:
                print('configuration!')
                return self.configuration(
                            setup.descriptor_index()
                        )
            case DescriptorTypes.STRING:
                return self.strings(
                        setup.descriptor_index(),
                        setup.language_id()
                    )
            case DescriptorTypes.INTERFACE:
                print('interface')
            case DescriptorTypes.ENDPOINT:
                print('endpoint')

    # SET_DESCRIPTOR
    def set_descriptor(self, setup):
        pass

    # GET_CONFIGURATION
    def get_configuration(self, setup):
        return None

    # SET_CONFIGURATION
    def set_configuration(self, setup):
        self._active_configuration = setup.configuration_value()
        return None

    def unknown(self, setup):
        """
        Unknown setup command!
        """
        print('unknown setup command')
