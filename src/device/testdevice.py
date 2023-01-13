from .basedevice import BaseDevice
from .speed import USBSpeed


class TestDevice(BaseDevice):
    """
    Device for testing this implementation.
    """
    VID = 0x1337
    PID = 0x1234

    def __init__(self):
        config = {
            'busnum': 1,
            'devnum': 1,
            'speed': USBSpeed.HIGH_SPEED.value,
            'idVendor': self.VID,
            'idProduct': self.PID,
            'bcdDevice': 1,
            'bDeviceClass': 0xff,
            'bDeviceSubClass': 0x7f,
            'bDeviceProtocol': 0x12,
            'bConfigurationValue': 0x01,
            'bNumConfigurations': 0x00
        }
        super().__init__(config, [])

    def command(self, data):
        #setup = USBSetup(data.setup)
        return None
