"""
Entrypoint.
"""
import click
from usbip import USBIPServer
from device.testdevice import TestDevice
from device.devicelist import DeviceList


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=3240)
def server(host, port):
    device_list = DeviceList()
    device_list.register('1-1', TestDevice())
    usb_server = USBIPServer(host, port, device_list)
    usb_server.start()
