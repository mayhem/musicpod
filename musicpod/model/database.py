# -*- coding: utf-8 -*-

from peewee import SqliteDatabase
from musicpod import DB_FILE

db = SqliteDatabase(DB_FILE, pragmas=(('foreign_keys', 'on'),))
