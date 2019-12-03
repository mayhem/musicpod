import os
from flask import Flask, render_template, flash, url_for, current_app, redirect
from flask_bootstrap import Bootstrap
import config
import json

STATIC_PATH = "/static"
STATIC_FOLDER = "../static"
TEMPLATE_FOLDER = "../templates"

app = Flask(__name__,
            static_url_path = STATIC_PATH,
            static_folder = STATIC_FOLDER,
            template_folder = TEMPLATE_FOLDER)
app.secret_key = config.SECRET_KEY

Bootstrap(app)

from musicpod.webserver.views.index import bp as index_bp
from musicpod.webserver.views.api import bp as api_bp
app.register_blueprint(index_bp)
app.register_blueprint(api_bp, url_prefix='/api')

# How do I limit this to only the index BP?
#@app.errorhandler(404)
#def page_not_found(message):
#    return render_template('errors/404.html', message=message), 404
