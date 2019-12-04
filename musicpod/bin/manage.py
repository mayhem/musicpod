#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from peewee import *
from musicpod.model.database import db
from musicpod.model.recording import Recording
from musicpod.scan.scan import ScanCollection
from musicpod import MUSIC_DIR, INDEX_DIR, DB_FILE
import click

import config

@click.group()
def cli():
    pass

@click.command()
def init_db():
    db.create_tables([Recording])
    try:
        os.makedirs(INDEX_DIR)
    except FileExistsError:
        pass

@click.command()
def run():
    from musicpod.webserver.app import app
    app.run(debug=True, host="0.0.0.0", port="5000")


@click.command()
def scan():
    sc = ScanCollection(DB_FILE, MUSIC_DIR, INDEX_DIR)
    try:
        sc.scan()
    except Exception:
        raise
        sys.exit(-1)

cli.add_command(init_db)
cli.add_command(run)
cli.add_command(scan)

def usage(command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))


if __name__ == "__main__":
    cli()
    sys.exit(0)
