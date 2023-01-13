# USB Device Emulator

Uses USB/IP to allow you to write custom devices, to test drivers or help with
reverse engineering.

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
