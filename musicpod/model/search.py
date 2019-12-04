# -*- coding: utf-8 -*-
from whoosh.fields import *
from whoosh.index import open_dir, EmptyIndexError
from musicpod import INDEX_DIR


schema = Schema(
    mbid=ID(stored=True), 
    name=TEXT(stored=True), 
    artist_mbid=TEXT(stored=True), 
    artist=TEXT(stored=True), 
    release_mbid=TEXT(stored=True), 
    release=TEXT(stored=True), 
    tnum=NUMERIC(stored=True), 
    duration=NUMERIC(stored=True), 
    content=TEXT)

ix = None

def open_search_index():
    global ix
    try:
        ix = open_dir(INDEX_DIR)
    except EmptyIndexError as err:
        print("cannot open search index: %s. Search will not function!" % err)
