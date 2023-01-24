import struct
from enum import Enum, Flag

from .exceptions import ParseError


class USBIPCmd(Enum):
    USBIP_CMD_SUBMIT = 0x00000001
    USBIP_RET_SUBMIT = 0x00000003
    USBIP_CMD_UNLINK = 0x00000002
    USBIP_RET_UNLINK = 0x00000004


class USBSubmitStatus(Enum):
    SUCCESS = 0
    FAILURE = 1


class USBIPUnlinkStatus(Enum):
    # 3426 is ECONNRESET, and this is the negation.
    SUCCESS = -3426
    FAILURE = 0


class USBIPDirection(Enum):
    USBIP_DIR_OUT = 0
    USBIP_DIR_IN = 1


class USBURBTransferFlags(Flag):
    USBIP_URB_SHORT_NOT_OK = 0x0001
    USBIP_URB_ISO_ASAP = 0x0002
    USBIP_URB_NO_TRANSFER_DMA_MAP = 0x0004
    USBIP_URB_ZERO_PACKET = 0x0040
    USBIP_URB_NO_INTERRUPT = 0x0080
    USBIP_URB_FREE_BUFFER = 0x0100
    USBIP_URB_DIR_IN = 0x0200
    USBIP_URB_DIR_OUT = 0
    # same as USBIP_URB_DIR_IN
    USBIP_URB_DIR_MASK = 0x0200

    USBIP_URB_DMA_MAP_SINGLE = 0x00010000
    USBIP_URB_DMA_MAP_PAGE = 0x00020000
    USBIP_URB_DMA_MAP_SG = 0x00040000
    USBIP_URB_MAP_LOCAL = 0x00080000
    USBIP_URB_SETUP_MAP_SINGLE = 0x00100000
    USBIP_URB_SETUP_MAP_LOCAL = 0x00200000
    USBIP_URB_DMA_SG_COMBINED = 0x00400000
    USBIP_URB_ALIGNED_TEMP_BUFFER = 0x00800000


class USBISOPacketDescriptor:
    """
    Isochronous transfer.

    Needs implementation
    """

    def __init__(self, _):
        pass


class USBIPHeaderBasic:
    def __init__(self, header):
        try:
            header_ = header[:20]
            command, seqnum, devid, direction, ep = struct.unpack(
                ">IIIII",
                header_
            )
            self.command = USBIPCmd(command)
            self.seqnum = seqnum
            self.devid = devid
            self.direction = direction
            self.ep = ep
        except struct.error:
            raise ParseError('Unable to unpack `usbip_header_basic`')


class USBIPCmdSubmit(USBIPHeaderBasic):
    def __init__(self, message):
        super().__init__(message)
        try:
            body = message[20:]
            before_seg = body[:20]
            transfer_flags, transfer_buffer_length, start_frame, \
                number_of_packets, interval = \
                struct.unpack('>IIIII', before_seg)

            setup_message = message[0x28:0x28+8]

            n = 0
            if self.direction == USBIPDirection.USBIP_DIR_OUT:
                n = transfer_buffer_length

            transfer_buffer = b''
            if n > 0:
                transfer_buffer = message[0x30:0x30+n]

            m = 0
            if number_of_packets != 0xffffffff or start_frame == 0:
                m = number_of_packets

            # attempt to read iso packets
            # TODO, this needs parsing!
            iso_packets = b''
            if m > 0:
                # call USBISOPacketDescriptor() on each one.
                iso_packets = body[0x30+n:0x30+n+m]

            # Write it out
            self.transfer_flags = USBURBTransferFlags(transfer_flags)
            self.transfer_buffer_length = transfer_buffer_length
            self.start_frame = start_frame
            self.number_of_packets = number_of_packets
            self.interval = interval
            self.setup = setup_message
            self.transfer_buffer = transfer_buffer
            self.iso_packets = iso_packets

        except struct.error:
            raise ParseError('Unable to unpack USBIP_CMD_SUBMIT')


class USBIPRetSubmit:
    def __init__(self, seqnum, status, data):
        self.data = data
        self.seqnum = seqnum
        self.status = status

    def pack(self):
        message = b''
        # header
        message += struct.pack('>I', USBIPCmd.USBIP_RET_SUBMIT.value)
        message += struct.pack('>I', self.seqnum)
        message += struct.pack('>I', 0)
        message += struct.pack('>I', 0)
        message += struct.pack('>I', 0)
        # body
        # status
        message += struct.pack('>I', self.status)
        # actual length
        message += struct.pack('>I', len(self.data))
        # start_frame
        message += struct.pack('>I', 0)
        # number_of_packets
        message += struct.pack('>I', 0) # 0xffffffff
        # error count
        message += struct.pack('>I', 0)
        # setup padding
        message += b'\x00'*8
        # transfer buffer
        message += self.data
        # iso_packet_descriptor

        return message


class USBIPCmdUnlink(USBIPHeaderBasic):
    def __init__(self, message):
        super().__init__(message)
        try:
            body = message[20:]
            unlink_seqnum = struct.unpack('>1I24x', body)
            self.unlink_seqnum = unlink_seqnum
        except struct.error:
            raise ParseError('Unable to unpack USBIP_CMD_UNLINK')


class USBIPRetUnlink:
    def __init__(self, seqnum, success):
        self.success = success
        self.seqnum = seqnum

    def pack(self):
        message = b''
        # header
        message += struct.pack('>I', USBIPCmd.USBIP_RET_UNLINK.value)
        message += struct.pack('>I', self.seqnum)
        message += struct.pack('>I', 0)
        message += struct.pack('>I', 0)
        message += struct.pack('>I', 0)

        # body
        if self.success:
            message += struct.pack('>I', USBIPUnlinkStatus.SUCCESS.value)
        else:
            message += struct.pack('>I', USBIPUnlinkStatus.FAILURE.value)

        # padding
        message += b'\x00'*24

        return message


def process_message(message):
    header = USBIPHeaderBasic(message[:0x14])
    res = None
    match header.command:
        case USBIPCmd.USBIP_CMD_SUBMIT:
            res = USBIPCmdSubmit(message)
        case USBIPCmd.USBIP_CMD_UNLINK:
            res = USBIPCmdUnlink(message)
        case _:
            pass
    return res
