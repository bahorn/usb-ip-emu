"""
Terrible Scapy USBMon implementation.
"""
from scapy.packet import Packet
from scapy.fields import \
        BitField, \
        ByteEnumField, \
        XByteField, \
        XByteEnumField, \
        ByteField, \
        XLELongField, \
        EnumField, \
        ConditionalField, \
        LESignedIntField, \
        StrFixedLenField, \
        LEIntField, \
        LEShortField, \
        XLEIntField, \
        LESignedLongField


_usbmon_types = {
    'S': 'URB_COMPLETE',
    'C': 'URB_COMPLETE',
    'E': 'URB_ERROR'
}


_usbmon_xfer_types = {
    0x00: 'URB_ISO',
    0x01: 'URB_INTERUPT',
    0x02: 'URB_CONTROL',
    0x03: 'URB_BULK',
    0x04: 'URB_UNKNOWN'
}


_usbmon_status = {
    0: 'SUCCESS',
    -115: 'EINPROGRESS'
}


class LESignedIntEnumField(EnumField[int]):
    """
    Scapy is missing this.
    """

    def __init__(self, name, default, enum):
        EnumField.__init__(self, name, default, enum, "<i")


class USBmon(Packet):
    name = "USBmon URB "
    # https://github.com/torvalds/linux/blob/master/Documentation/usb/usbmon.rst#raw-binary-format-and-api
    fields_desc = [
        XLELongField("id", 0),
        XByteEnumField("type", 0xFF, _usbmon_types),
        ByteEnumField("xfer_type", 0xFF, _usbmon_xfer_types),
        BitField("transfer_direction", 0, 4),
        BitField("epnum", 0, 4),
        ByteField("devnum", 0),
        LEShortField("busnum", 0),
        XByteField("flag_setup", 0),
        XByteField("flag_data", 0),
        LESignedLongField("ts_sec", 0),
        LESignedIntField("ts_usec", 0),
        LESignedIntEnumField("status", 0, _usbmon_status),
        LEIntField("length", 0),
        LEIntField("len_cap", 0),

        # setup
        ConditionalField(
            StrFixedLenField("setup", 0, 8),
            lambda pkt: pkt.xfer_type == 0x02
        ),

        # iso_rec struct
        ConditionalField(
            LESignedIntField("iso_rec_error_count", 0),
            lambda pkt: pkt.xfer_type == 0x00
        ),
        ConditionalField(
            LESignedIntField("iso_rec_numdesc", 0),
            lambda pkt: pkt.xfer_type == 0x00
        ),

        # unused
        ConditionalField(
            StrFixedLenField("unused", 0, 8),
            lambda pkt: pkt.xfer_type not in [0x00, 0x02]
        ),

        LESignedIntField("interval", 0),
        LESignedIntField("start_frame", 0),
        XLEIntField("xfer_flags", 0),
        LEIntField("ndesc", 0)
    ]


_b_request = {
    0x00: 'GET_STATUS',
    0x01: 'CLEAR_FEATURE',
    0x03: 'SET_FEATURE',
    0x05: 'SET_ADDRESS',
    0x06: 'GET_DESCRIPTOR',
    0x07: 'SET_DESCRIPTOR',
    0x08: 'GET_CONFIGURATION',
    0x09: 'SET_CONFIGURATION'
}


class SetupPacket(Packet):
    name = "USB Setup"

    fields_desc = [
        ByteField('bmRequestType', 0),
        ByteEnumField('bRequest', 0, _b_request),

        # GET_DESCRIPTOR wValue
        ConditionalField(
            ByteField("descriptor_index", 0),
            lambda pkt: pkt.bRequest == 0x06
        ),
        ConditionalField(
            ByteField("descriptor_type", 0),
            lambda pkt: pkt.bRequest == 0x06
        ),

        ConditionalField(
            LEShortField('wValue', 0),
            lambda pkt: pkt.bRequest != 0x06
        ),
        LEShortField('wIndex', 0),
        LEShortField('wLength', 0)
    ]


class StringDescriptor(Packet):
    name = "USB String Descriptor"

    fields_desc = [
        ByteField('bLength', 0),
        ByteField('bDescriptorType', 0x03)
    ]


class DeviceDescriptor(Packet):
    name = "USB Device Descriptor"

    fields_desc = [
        ByteField('bLength', 0),
        ByteField('bDescriptorType', 0x01),
        LEShortField('bcdUSB', 0x0000),
        ByteField('bDeviceClass', 0x00),
        ByteField('bDeviceSubClass', 0x00),
        ByteField('bDeviceProtocol', 0x00),
        ByteField('bMaxPacketSize', 64),
        LEShortField('idVendor', 0x0000),
        LEShortField('idProduct', 0x0000),
        LEShortField('bcdDevice', 0x0000),
        ByteField('iManufacturer', 0x00),
        ByteField('iProduct', 0x00),
        ByteField('iSerialNumber', 0x00),
        ByteField('bNumConfigurations', 0x00)
    ]
