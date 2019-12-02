# -*- coding: utf-8 -*-

from musicpod.model.recording import Recording
import mutagen
import mutagen.mp3

def read(file, mtime):

    mdata = { 'mtime' : mtime }

    tags = None
    try:
        tags = mutagen.mp3.MP3(file)
    except mutagen.mp3.HeaderNotFoundError:
        print("Cannot read metadata from file %s" % file.encode('utf-8'))
        return None

    mdata['duration'] = int(tags.info.length * 1000)
    if 'TPE1' in tags: 
        mdata['artist'] = str(tags['TPE1'])
    else:
        mdata['artist'] = unknownString

    if 'TSOP' in tags: 
        mdata['sortname'] = str(tags['TSOP'])
    else:
        if 'XSOP' in tags: 
            mdata['sortname'] = str(tags['XSOP'])
        else:
            mdata['sortname'] = ""

    if 'TALB' in tags: 
        mdata['release'] = str(tags['TALB'])
    else:
        mdata['release'] = unknownString

    if 'TXXX:MusicBrainz Album Artist' in tags: 
        mdata['release_artist'] = unicode(tags['TXXX:MusicBrainz Album Artist'])
    else:
        mdata['release_artist'] = ''

    if 'TIT2' in tags: 
        mdata['recording'] = str(tags['TIT2'])
    else:
        mdata['recording'] = unknownString

    if 'TDRC' in tags: 
        try:
            mdata['year'] = int(str(tags['TDRC']))
        except ValueError:
            mdata['year'] = 0
    else:
        mdata['year'] = 0

    if 'TRCK' in tags: 
        mdata['tnum'] = str(tags['TRCK'])
        if str(mdata['tnum']).find('/') != -1: 
            mdata['tnum'], dummy = str(mdata['tnum']).split('/')
        try:
            mdata['tnum'] = int(mdata['tnum'])
        except ValueError:
            mdata['tnum'] = 0
    else:
        mdata['tnum'] = 0

    if 'TXXX:MusicBrainz Artist Id' in tags: 
        id = str(tags['TXXX:MusicBrainz Artist Id'])
        # sometimes artist id fields contain two ids. For now, pick the first one and go
        ids = id.split('/')
        mdata['artist_mbid'] = ids[0]
    else:
        mdata['artist_mbid'] = ''

    if 'UFID:http://musicbrainz.org' in tags: 
        mdata['recording_mbid'] = tags['UFID:http://musicbrainz.org'].data.decode('utf-8')
    else:
        mdata['recording_mbid'] = ''

    if 'TXXX:MusicBrainz Album Id' in tags: 
        mdata['release_mbid'] = str(tags['TXXX:MusicBrainz Album Id'])
    else:
        mdata['release_mbid'] = ''

    if 'TXXX:MusicBrainz Album Artist Id' in tags: 
        mdata['release_artist_mbid'] = str(tags['TXXX:MusicBrainz Album Artist Id'])
    else:
        mdata['release_artist_mbid'] = ''

    return mdata
