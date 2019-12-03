import os
import sys
import uuid
import peewee
from flask import Flask, jsonify, Blueprint, send_from_directory
from werkzeug.exceptions import BadRequest, NotFound, ServiceUnavailable
from musicpod.model.recording import Recording
import config

bp = Blueprint('api', __name__)

def sanity_check_and_load_recording(mbid):
    try:
        uuid.UUID(mbid)
    except ValueError:
        raise BadRequest

    try:
        print(mbid)
        recording = Recording.get(Recording.mbid == mbid)
    except peewee.DoesNotExist as err:
        raise NotFound

    if not os.path.exists(os.path.join(config.MUSIC_DIR, recording.path)):
        raise ServiceUnavailable

    return recording


@bp.route('/recording/<mbid>')
def recording(mbid):
    recording = sanity_check_and_load_recording(mbid)
    print(recording.path)
    return send_from_directory(config.MUSIC_DIR, recording.path)


@bp.route('/recording/<mbid>/metadata')
def metadata(mbid):

    recording = sanity_check_and_load_recording(mbid)
    return jsonify({
        "mbid" : recording.mbid,
        "artist_name" : recording.artist_name,
        "artist_mbid" : recording.artist_mbid,
        "release_name" : recording.release_name,
        "release_mbid" : recording.release_mbid,
        "name" : recording.name,
        "duration" : recording.duration or 0,
        "tnum" : recording.tnum
    })


