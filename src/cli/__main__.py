"""
Entrypoint.
"""
import logging
import click

from commands.server import server
from commands.pcap import pcap
from commands.emulate import emulate

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    level=logging.INFO
)


@click.group()
def main():
    pass


main.add_command(server)
main.add_command(pcap)
main.add_command(emulate)


if __name__ == "__main__":
    main()
