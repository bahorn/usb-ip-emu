"""
Entrypoint.
"""
import logging
import click

from commands.server import server

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    level=logging.INFO
)


@click.group()
def main():
    pass


main.add_command(server)

if __name__ == "__main__":
    main()
