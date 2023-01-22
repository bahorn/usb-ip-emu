"""
Configuration of a USB Device.
"""
from bitarray import bitarray
from .descriptors import ConfigurationDescriptor


class Configuration:
    def __init__(self, index, name_idx=0, remote_wakeup=False,
                 self_powered=True, max_power=100):
        self.interfaces = []
        self._index = index
        self._name_idx = name_idx
        # default is 100ma, as it works in multiples of 2.
        self._max_power = int(max_power / 2)
        self._remote_wakeup = remote_wakeup
        self._self_powered = self_powered

    def add_interface(self, interface):
        """
        Add an interface to this configuration.
        """
        self.interfaces.append(interface)

    def attributes(self):
        """
        Attributes as a bitmap
        """
        resp = bitarray()

        resp += [1]
        resp += [self._self_powered]
        resp += [self._remote_wakeup]
        resp += [0, 0, 0, 0, 0]

        return resp

    def descriptor(self):
        """
        Get a descriptor for this configuration
        """
        # Size of a configuration descriptor
        total_length = 9
        # Interfaces are of a fixed size
        total_length += len(self.interfaces) * 9
        # Sum up the number of endpoints.
        for interface in self.interfaces:
            total_length += 7 * len(interface.endpoints())

        reply = []
        reply.append(ConfigurationDescriptor(
            {
                'wTotalLength': total_length,
                'bNumInterfaces': len(self.interfaces),
                'bConfigurationValue': self._index,
                'iConfiguration': self._name_idx,
                'bmAttributes': int.from_bytes(self.attributes(), 'little'),
                'bMaxPower': self._max_power
            }
        ))
        for interface in self.interfaces:
            reply.append(interface.descriptor())
            # now get the endpoints.
            for endpoint in interface.endpoints():
                reply.append(endpoint.descriptor())

        return reply
