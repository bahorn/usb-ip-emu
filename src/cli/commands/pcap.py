"""
Commands to handle pcaps.
"""
import click
from analysis.analysis import PCAPAnalysis


@click.command()
@click.argument('files', nargs=-1)
def config_dump(files):
    analysis = PCAPAnalysis(files)
    analysis.configuration()
    print(analysis.device())
    print(analysis.strings())


@click.group()
def pcap():
    pass


pcap.add_command(config_dump)
