"""
Entrypoint.
"""
import click
import os
from usbip import USBIPServer
from devices.emulateddevice import EmulatedDevice
from device.devicelist import DeviceList


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=3240)
@click.argument('pcaps', nargs=-1)
def emulate(host, port, pcaps):
    device_list = DeviceList()

    # support either pcapng's or directories with pcapngs.
    pcaps_ = []
    for pcap in pcaps:
        if not os.path.isdir(pcap):
            pcaps_.append(pcap)
            continue

        for result in os.listdir(pcap):
            pcaps_.append(os.path.join(pcap, result))

    if len(pcaps_) == 0:
        return

    emulated_device = EmulatedDevice(pcaps_)
    device_list.register((1, 1), emulated_device)
    usb_server = USBIPServer(host, port, device_list)
    usb_server.start()
