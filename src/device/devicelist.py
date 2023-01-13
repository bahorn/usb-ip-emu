"""
Implementation of a device list.
"""


class DeviceList:
    """
    Device List, allowing registering devices and then packing them in a form
    that can be sent over the network.
    """

    def __init__(self):
        self._devices = {}

    def register(self, busid, device):
        self._devices[busid] = device

    def unregister(self, busid):
        del self._devices[busid]

    def lookup(self, busid):
        return self._devices.get(busid)

    def devices(self):
        return self._devices.keys()
