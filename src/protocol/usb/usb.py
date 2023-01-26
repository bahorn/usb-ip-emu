"""
Abstract representation of a USB packet.

The different protocol layers need to generate these, for sections like
analysis to work.
"""
from .setup import process_USB_setup


class USBPacket:
    def __init__(self, xfer_type, endpoint, setup, payload):
        self.xfer_type = xfer_type
        self.endpoint = endpoint
        self.setup = process_USB_setup(setup)
        self.payload = payload
