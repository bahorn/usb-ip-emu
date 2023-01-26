"""
Entrypoint.
"""
import binascii
import click
import os
import logging
from pytermgui import tim

from usbip import USBIPServer
from devices.emulateddevice import EmulatedDevice
from device.devicelist import DeviceList


def hex_pad(value, padding=6):
    return f"{value:#0{padding}x}"


def hexdump(data):
    cur = ""
    rows = []
    payload = binascii.hexlify(data, ' ', 2).decode('ascii').split(' ')
    for idx, bytes in enumerate(payload):
        if idx % 16 == 0 and idx != 0:
            rows.append(cur)
            cur = ""
        cur += payload[idx]
        cur += ' '

    if cur:
        rows.append(cur)

    return rows


def pre_response(packet):
    wvalue = hex_pad(packet.setup.wValue())
    windex = hex_pad(packet.setup.wIndex())
    wlength = packet.setup.wLength()
    name = packet.setup.__class__.__name__
    tim.print(f'[@primary #auto] ENDPOINT {packet.endpoint} ')
    tim.print(
        ''.join([
            '[@secondary #auto bold] SETUP ',
            f'[@surface #auto] {name} ',
            f'[@surface-1 #auto] {wvalue} ',
            f'[@surface-2 #auto] {windex} ',
            f'[@surface-3 #auto] {wlength:#03} '
         ])
    )
    if packet.payload:
        payload = hexdump(packet.payload)
        tim.print(f'[@tertiary #auto bold] PAYLOAD ({len(packet.payload)})')
        for row in payload:
            tim.print(f'> {row} ')
    print()


def recommendation(packet, choice):
    best = choice[0]
    dist = best[0]
    reply = best[1]['C']
    lenmsg = reply.payload if len(reply.payload) else 'EMPTY REPLY'

    tim.print(f'[@primary #auto bold] RESPONSE ({lenmsg}) ')
    tim.print(f'[@secondary #auto bold] Distance [@surface #auto] {dist}')

    if reply.payload:
        payload = hexdump(reply.payload)
        tim.print(f'[@tertiary #auto bold] PAYLOAD ({len(reply.payload)})')
        for row in payload:
            tim.print(f'> {row} ')
    print()


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
        'recommendation': recommendation
    }

    emulated_device = EmulatedDevice(pcaps_, callbacks)

    device_list.register((1, 1), emulated_device)
    usb_server = USBIPServer(host, port, device_list)
    usb_server.start()
