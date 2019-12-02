# -*- coding: utf-8 -*-

from peewee import SqliteDatabase
from config import DB_FILE

db = SqliteDatabase(DB_FILE, pragmas=(('foreign_keys', 'on'),))
