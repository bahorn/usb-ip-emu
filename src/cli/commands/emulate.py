"""
Entrypoint.
"""
import click
import os
from usbip import USBIPServer
from devices.emulateddevice import EmulatedDevice
from device.devicelist import DeviceList


def pre_response(packet):
    #print(packet.setup.wValue())
    pass


def post_response(packet, response):
    #print(response)
    pass

def recommendation(packet, choice):
    #print(choice)
    pass

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

    callbacks = {
        'pre_response': pre_response,
        'post_response': post_response,
        'recommendation': recommendation
    }
    emulated_device = EmulatedDevice(pcaps_, callbacks)

    device_list.register((1, 1), emulated_device)
    usb_server = USBIPServer(host, port, device_list)
    usb_server.start()
