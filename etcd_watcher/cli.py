# -*- coding: utf-8 -*-

"""Console script for etcd_watcher."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for etcd_watcher."""
    click.echo("Replace this message by putting your code into "
               "etcd_watcher.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
