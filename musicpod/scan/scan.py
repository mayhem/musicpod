#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import datetime
import sys

from musicpod.model.database import db
from musicpod.model.recording import Recording
from musicpod.scan import mp3
from musicpod.scan import flac
from config import DB_FILE
import peewee

SUPPORTED_FORMATS = ["mp3", "flac"]

class ScanCollection(object):
    ''' 
    Scan a given path and enter/update the metadata in the database
    '''

    def __init__(self, music_dir):
        self.music_dir = music_dir

    def scan(self):
        # Keep some stats
        self.total = 0
        self.no_id = 0
        self.not_changed = 0
        self.updated = 0
        self.added = 0
        self.error = 0
        self.skipped = 0
        self.duplicated = 0
        self.moved = 0

        if not os.path.exists(DB_FILE):
            print("Music database file does not exist. please create it first.")
            sys.exit(-1)

        db.connect()
        self.traverse(self.music_dir)

        print("Checked %s tracks" % self.total)
        print("  %d tracks not changed since last run" % self.not_changed)
        print("  %d tracks added" % self.added)
        print("  %d tracks updated" % self.updated)
        print("  %d tracks moved" % self.moved)
        print("  %d tracks could not be read" % self.error)
        print("  %d tracks have no MusicBrainz id" % self.no_id)
        print("  %d files are not supported" % self.skipped)
        print("  %d duplicated and ignored" % self.duplicated)
        if self.total != self.not_changed + self.updated + self.added + self.error + self.skipped + self.duplicated + self.moved:
            print("And for some reason these numbers don't add up to the total number of tracks. Hmmm.")

    def traverse(self, relative_path):

        fullpath = os.path.join(self.music_dir, relative_path)
        for f in os.listdir(fullpath):
            if f in ['.', '..']: 
                continue

            item = os.path.join(relative_path, f)
            if os.path.isfile(item): 
                self.add(item)
            if os.path.isdir(item): 
                if not self.traverse(item):
                    return False

        return True


    def add(self, relative_path):

        fullpath = os.path.join(self.music_dir, relative_path)
        self.total += 1

        # Check to see if the file in question has changed since the last time
        # we looked at it. If not, skip it for speed
        stats = os.stat(fullpath)
        ts = datetime.datetime.fromtimestamp(stats[8])

        base, ext = os.path.splitext(relative_path)
        ext = ext.lower()[1:]
        base = os.path.basename(relative_path)
        if ext not in SUPPORTED_FORMATS:
            print("    ? %s" % base)
            self.skipped += 1
            return

        exists = False
        try:
            recording = Recording.get(Recording.path == relative_path)
        except peewee.DoesNotExist as err:
            recording = None

        if recording:
            exists = True
            if recording.mtime == ts:
                self.not_changed += 1
                print("    - %s" % base)
                return
        
        rec, status = self.add_to_or_update_database(relative_path, ext, ts, exists)
        if status == "duplicate":
            print("    D %s" % base)
            self.duplicated +=1
        elif status == "moved":
            print("    M %s" % base)
            self.moved += 1
        elif status == "updated":
            print("    U %s" % base)
            self.updated += 1
        elif status == "added":
            print("    A %s" % base)
            self.added += 1
        elif status == "noid`":
            print("    X %s" % base)
            self.no_id +=1
        else:
            self.error += 1
            print("    E %s" % base)


    def add_metadata_to_db(self, mdata, path):

        status = "error"
        with db.atomic() as transaction:
            try:
                recording = Recording.select().where(Recording.mbid == mdata['recording_mbid']).get()
                if not os.path.exists(os.path.join(self.music_dir, recording.path)):
                    rec, dummy =  self.update_metadata_in_db(mdata, path)
                    return rec, "moved"
                else:
                    status = "duplicate"
                    return recording, status
            except peewee.DoesNotExist:
                status = "added"

            recording = Recording.create(path = path,
                mbid = mdata['recording_mbid'],
                name = mdata['recording'],
                artist_name = mdata['artist'],
                artist_mbid = mdata['artist_mbid'],
                release_name = mdata['release'],
                release_mbid = mdata['release_mbid'],
                mtime = mdata['mtime'],
                tnum = mdata['tnum'])

        return recording, status


    def update_metadata_in_db(self, mdata, path):

        with db.atomic() as transaction:
            try:
                recording = Recording.select().where(Recording.mbid == mdata['recording_mbid']).get()
            except peewee.DoesNotExist:
                return None, "error"

            recording.path = path
            recording.mbid = mdata['recording_mbid']
            recording.name = mdata['recording']
            recording.artist_name = mdata['artist']
            recording.artist_mbid = mdata['artist_mbid']
            recording.release_name = mdata['release']
            recording.release_mbid = mdata['release_mbid']
            recording.mtime = mdata['mtime']
            recording.tnum = mdata['tnum']
            recording.save()

        return recording, "updated"

    def add_to_or_update_database(self, relative_path, format, mtime, update):
        if format == "mp3":
            mdata = mp3.read(os.path.join(self.music_dir, relative_path), mtime)
        elif format == "flac":
            mdata = flac.read(os.path.join(self.music_dir, relative_path), mtime)

        if not mdata['recording_mbid']:
            return None, "noid"

        if update:
            return self.update_metadata_in_db(mdata, relative_path)
        else:
            return self.add_metadata_to_db(mdata, relative_path)
