from peewee import *
from musicpod.model.database import db

class Recording(Model):
    """
    Basic metadata information about a recording.
    """

    class Meta:
        database = db

    id = AutoField()
    mbid = UUIDField(index=True, unique=True)
    artist_name = TextField(null = False)
    artist_mbid = UUIDField(index=True)
    release_name = TextField(null = False)
    release_mbid = UUIDField(index=True)
    name = TextField(null = False)
    path = TextField(null = False)
    mtime = TimestampField(null = False)
    duration = IntegerField(null = True)
    tnum = IntegerField(null = True)

    def __repr__(self):
        return "<Recording('%s','%s')>" % (self.mbid, self.name)
