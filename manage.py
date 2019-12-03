#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
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
    try:
        os.makedirs(config.INDEX_DIR)
    except FileExistsError:
        pass

@click.command()
def run():
    from musicpod.webserver.app import app
    app.run(debug=True, host="0.0.0.0", port="5000")

cli.add_command(init_db)
cli.add_command(run)

def usage(command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))


if __name__ == "__main__":
    cli()
    sys.exit(0)
