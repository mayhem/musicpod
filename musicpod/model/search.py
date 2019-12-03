# -*- coding: utf-8 -*-
from whoosh.fields import *

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
