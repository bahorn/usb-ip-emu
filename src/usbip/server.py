"""
The server.

Based on:
* https://docs.kernel.org/usb/usbip_protocol.html
"""
# import binascii
import logging
from enum import Enum
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

from .message import \
        USBIPClientMessage, \
        USBIPCommands, \
        USBIPReplyDevlist, \
        USBIPReplyImport

from protocol.usb import USBPacket
from .usbip import process_message, USBIPCmd, USBIPRetUnlink, USBIPRetSubmit


USBIPState = Enum('USBIPState', ['OP', 'USBIP'])


class USBIP(Protocol):
    """
    Server side of the USBIP implementation.
    """

    def __init__(self, devlist):
        self.devlist = devlist
        self.state = USBIPState.OP
        self.device = None
        super().__init__()

    def connectionMade(self):
        pass

    def connectionLost(self, reason):
        pass

    def dataReceived(self, data):
        logging.debug('Message Recieved')
        match self.state:
            case USBIPState.OP:
                self.operation(data)
            case USBIPState.USBIP:
                self.command(data)

    def operation(self, data):
        message = USBIPClientMessage(data)
        match message.cc:
            case USBIPCommands.OP_REQ_DEVLIST:
                logging.info('requesting devlist')
                # sending the devlist, then kill the connection.
                reply = USBIPReplyDevlist(self.devlist)
                self.transport.write(reply.pack())
                self.transport.loseConnection()

            case USBIPCommands.OP_REQ_IMPORT:
                logging.info(f'importing {message.busid}')
                busid = str(message.busid)

                busid_ = tuple(map(int, busid.split('-')))

                # if the device exists, we can transisition over to
                # the usbip case and process those packets.
                self.device = self.devlist.lookup(busid_)
                # now send a message based on if this device lookup was
                # succesful.
                reply = USBIPReplyImport(busid, self.device)
                self.transport.write(reply.pack())

                if self.device:
                    self.state = USBIPState.USBIP
                else:
                    self.transport.loseConnection()

            case _:
                logging.error('unknown command?')

    def command(self, data):
        if not self.device:
            return
        res = process_message(data)
        if res:
            match res.command:
                case USBIPCmd.USBIP_CMD_SUBMIT:
                    usb_packet = USBPacket(
                        0, res.ep, res.setup, res.transfer_buffer
                    )
                    # All zero setup packets are just worth ignoring it seems.
                    # avoids an annoying bug where the host will spam URBs.
                    if usb_packet.setup.bytes == b'\x00'*8:
                        return
                    # now let the device process the message
                    response = self.device.command(usb_packet)
                    # decide how we pack this.
                    if response:
                        self.transport.write(
                            USBIPRetSubmit(
                                res.seqnum, 0, response.pack()
                            ).pack()
                        )
                    else:
                        self.transport.write(
                            USBIPRetSubmit(res.seqnum, -32, b'').pack()
                        )
                case USBIPCmd.USBIP_CMD_UNLINK:
                    return self.transport.write(
                            USBIPRetUnlink(res.seqnum, 0).pack()
                    )


class USBIPFactory(Factory):
    def __init__(self, devlist):
        self.devlist = devlist
        super().__init__()

    def buildProtocol(self, addr):
        return USBIP(self.devlist)


class USBIPServer:
    """
    Wrapper around the Twisted Server.
    """

    def __init__(self, host, port, device_list):
        self.endpoint = TCP4ServerEndpoint(reactor, port, interface=host)
        self.devlist = device_list

    def start(self):
        logging.info('Starting Server')
        self.endpoint.listen(USBIPFactory(self.devlist))
        reactor.run()
