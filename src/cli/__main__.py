"""
Entrypoint.
"""
import logging
import click
from usbip import USBIPServer
from device.testdevice import TestDevice
from device.devicelist import DeviceList

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    level=logging.INFO
)


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=3240)
def server(host, port):
    device_list = DeviceList()
    device_list.register('1-1', TestDevice())
    usb_server = USBIPServer(host, port, device_list)
    usb_server.start()


@click.group()
def main():
    pass


main.add_command(server)

if __name__ == "__main__":
    main()
