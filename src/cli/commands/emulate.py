"""
Entrypoint.
"""
import click
from usbip import USBIPServer
from devices.emulateddevice import EmulatedDevice
from device.devicelist import DeviceList


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=3240)
@click.argument('pcaps', nargs=-1)
def emulate(host, port, pcaps):
    device_list = DeviceList()
    emulated_device = EmulatedDevice(pcaps)
    device_list.register((1, 1), emulated_device)
    usb_server = USBIPServer(host, port, device_list)
    usb_server.start()
