from flask import Flask, jsonify, Blueprint

bp = Blueprint('api', __name__)

@bp.route('/recording/<mbid>')
def recording(mbid):
    return jsonify({})
