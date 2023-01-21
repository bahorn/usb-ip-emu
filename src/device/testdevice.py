from .basedevice import BaseDevice
from .speed import USBSpeed


class TestDevice(BaseDevice):
    """
    Device for testing this implementation.
    """
    VID = 0x1038
    PID = 0x150d

    def __init__(self):
        config = {
            'busnum': 1,
            'devnum': 1,
            'speed': USBSpeed.HIGH_SPEED.value,
            'idVendor': self.VID,
            'idProduct': self.PID,
            'bcdDevice': 0x0102,
            'bDeviceClass': 0x00,
            'bDeviceSubClass': 0x00,
            'bDeviceProtocol': 0x00,
            'bConfigurationValue': 0x00,
            'bNumConfigurations': 1
        }
        super().__init__(config, [])
