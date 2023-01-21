# USB Soulkiller

Uses USB/IP to allow you to write emulate USB devices.
Either custom or based off packet captures, for the purpose of reverse
engineering or debugging.

Name is from the Lore in Mike Pondsmith's Cyberpunk, where the SoulKiller is a
program that copies someones mind. (Which I thought fit with copying USB
devices!)

## Usage

### Setup

Use poetry to install the dependencies with:
```
poetry install
```

Then run the server with:

```
poetry run python3 src/cli server
```

### Connecting a Ubuntu Machine to this

Setup USB/IP;
```
sudo apt install linux-tools-generic linux-tools-`uname -r`
sudo modprobe vhci-hcd
```

Then you can connect it to this with:

```
usbip list -r HOSTNAME
sudo usbip attach -r HOSTNAME -b INTERFACE
```

HOSTNAME is the machine you are running this on.


## Useful Documentation

* USB/IP protocol - https://docs.kernel.org/usb/usbip_protocol.html

Side note on this, I believe the following in it is incorrect:

> number_of_packets: number of ISO packets; shall be set to 0xffffffff if not
> ISO transfer 

Actual implementations set it to 0, including wiresharks disector and the
kernels code, unless I misunderstood something.

* USB in a NutShell - https://www.beyondlogic.org/usbnutshell/usb1.shtml

Great docs.

* USB Made Simple - https://www.usbmadesimple.co.uk/ums_4.htm

Good docs, found some things easier to pick up upon here the beyondlogics docs.

## Debugging

### Wireshark

If you want to analyze the traffic with wireshark:

* Make sure the dissector is enabled (Analyze->Enabled Protocols, select USBIP)
* Set the port with Edit->Preferences->Protocols->USBIP to 3240 (or whatever you
  are using).
