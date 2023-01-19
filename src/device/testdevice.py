from .basedevice import BaseDevice
from .descriptors import DeviceDescriptor
from .speed import USBSpeed
from .setup import process_USB_setup, DeviceGetDescriptor
from usbip.usbip import USBIPCmd


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
            'bcdDevice': 0x102,
            'bDeviceClass': 0x00,
            'bDeviceSubClass': 0x00,
            'bDeviceProtocol': 0x00,
            'bConfigurationValue': 0x00,
            'bNumConfigurations': 0x00
        }
        super().__init__(config, [])

    def command(self, packet):
        """
        Process an URB for this device.
        """

        setup = process_USB_setup(packet.setup)
        if isinstance(setup, DeviceGetDescriptor):
            # respond with the descriptor
                return self.descriptor()


        return None
