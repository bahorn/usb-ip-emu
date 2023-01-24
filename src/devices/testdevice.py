from device.basedevice import BaseDevice
from device.configuration import Configuration
from device.endpoint import Endpoint
from device.interface import Interface
from device.strings import Strings, Languages
from device.enum import USBSpeed


class TestDevice(BaseDevice):
    """
    Device for testing this implementation.
    """
    VID = 0x1337
    PID = 0x1234

    def __init__(self):
        endpoint1 = Endpoint(1, 64, 1)
        endpoint2 = Endpoint(2, 64, 1)

        interface1 = Interface(0, name_idx=2)
        interface1.add_endpoints([endpoint1, endpoint2])
        config1 = Configuration(1)
        config1.add_interface(interface1)

        self._configurations = {0: config1}
        self._strings = Strings([Languages.ENGLISH_US.value])
        self._strings.set_strings(
                Languages.ENGLISH_US.value, ['Hello world1', 'Hello world2']
            )

        config = {
            'idVendor': self.VID,
            'idProduct': self.PID,
            'bcdDevice': 0x0102,
            'bDeviceClass': 0x00,
            'bDeviceSubClass': 0x00,
            'bDeviceProtocol': 0x00
        }
        super().__init__(config)
        self._active_configuration = 1
