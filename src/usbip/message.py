"""
Implementation of the USBIP message format.

https://docs.kernel.org/usb/usbip_protocol.html
"""
import struct
from enum import Enum
from .exceptions import ParseError, VersionError

# from device.devicelist import DeviceList

USBIP_VERSION = 0x0111


class USBIPCommands(Enum):
    """
    These are the commands to setup the USB IP connection.

    After calling OP_REQ_IMPORT, this uses a different command format.
    """
    OP_REQ_DEVLIST = 0x8005
    OP_REP_DEVLIST = 0x0005
    OP_REQ_IMPORT = 0x8003
    OP_REP_IMPORT = 0x0003


class USBIPClientMessage:
    """
    Client Message Format for the OP_REQ_* messages.
    """

    def __init__(self, data):
        try:
            version, cc, status = struct.unpack('>HHI', data[:8])
            self.version = version
            self.cc = USBIPCommands(cc)
            self.status = status

            if self.version != USBIP_VERSION:
                raise VersionError(
                    f'Version {self.version} != {USBIP_VERSION}'
                )

            if self.cc == USBIPCommands.OP_REQ_IMPORT:
                self.busid = struct.unpack('>32s', data[8:8+32])
                self.busid = self.busid[0].decode('ascii').strip('\x00')


        except struct.error:
            raise ParseError(
                'Unable to unpack the OP_REQ message'
            )


def fake_path(busid):
    return f'/dev/fake/{busid}'


class USBIPReplyDevlist:
    """
    Reply to a devlist request with a given devlist.
    """

    def __init__(self, devlist):
        self.devlist = devlist

    def pack(self):
        message = b''
        message += struct.pack('>H', USBIP_VERSION)
        message += struct.pack('>H', USBIPCommands.OP_REP_DEVLIST.value)
        message += struct.pack('>I', 0x00)
        message += struct.pack('>I', len(self.devlist.devices()))

        for busid in self.devlist.devices():
            device = self.devlist.lookup(busid)
            device_info = b''
            # fake a path, as we are dealing with virtual devices.
            device_info += struct.pack(
                    '256s',
                    bytes(fake_path(busid), 'ascii')
            )
            device_info += struct.pack('32s', bytes(busid, 'ascii'))
            device_info += struct.pack('>I', device.busnum())
            device_info += struct.pack('>I', device.devnum())
            device_info += struct.pack('>I', device.speed())
            device_info += struct.pack('>H', device.idVendor())
            device_info += struct.pack('>H', device.idProduct())
            device_info += struct.pack('>H', device.bcdDevice())
            device_info += struct.pack('>B', device.bDeviceClass())
            device_info += struct.pack('>B', device.bDeviceSubClass())
            device_info += struct.pack('>B', device.bDeviceProtocol())
            device_info += struct.pack('>B', device.bConfigurationValue())
            device_info += struct.pack('>B', device.bNumConfigurations())
            device_info += struct.pack('>B', device.bNumInterfaces())
            # get the interface information
            for interface in device.interfaces():
                interface_info = b''
                interface_info += struct.pack(
                        '>B', interface.bInterfaceClass()
                )
                interface_info += struct.pack(
                        '>B', interface.bInterfaceSubClass()
                )
                interface_info += struct.pack(
                        '>B', interface.bInterfaceProtocol()
                )
                interface_info += b'\x00'
                device_info += interface_info
            message += device_info

        return message


class USBIPReplyImport:
    """
    Reply to a import message
    """

    def __init__(self, busid, device):
        self.device = device
        self.busid = busid

    def pack(self):
        message = b''
        message += struct.pack('>H', USBIP_VERSION)
        message += struct.pack('>H', USBIPCommands.OP_REP_IMPORT.value)
        message += struct.pack('>I', 0 if self.device else 1)

        # check if we have a device or not.
        if not self.device:
            return message

        device_info = b''
        # fake a path, as we are dealing with virtual devices.
        device_info += struct.pack(
                '256s',
                bytes(fake_path(self.busid), 'ascii')
        )
        device_info += struct.pack('32s', bytes(self.busid, 'ascii'))
        device_info += struct.pack('>I', self.device.busnum())
        device_info += struct.pack('>I', self.device.devnum())
        device_info += struct.pack('>I', self.device.speed())
        device_info += struct.pack('>H', self.device.idVendor())
        device_info += struct.pack('>H', self.device.idProduct())
        device_info += struct.pack('>H', self.device.bcdDevice())
        device_info += struct.pack('>B', self.device.bDeviceClass())
        device_info += struct.pack('>B', self.device.bDeviceSubClass())
        device_info += struct.pack('>B', self.device.bDeviceProtocol())
        device_info += struct.pack('>B', self.device.bConfigurationValue())
        device_info += struct.pack('>B', self.device.bNumConfigurations())
        device_info += struct.pack('>B', self.device.bNumInterfaces())

        message += device_info
        return message
