#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from peewee import *
from musicpod.model.database import db
from musicpod.model.recording import Recording
import click

import config

@click.group()
def cli():
    pass

@click.command()
def init_db():
    db.create_tables([Recording])

cli.add_command(init_db)

def usage(command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))


if __name__ == "__main__":
    cli()
    sys.exit(0)
