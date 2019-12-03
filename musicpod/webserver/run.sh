#!/bin/sh

export FLASK_APP=app
export FLAK_ENV=development
export FLASK_DEBUG=1
export FLASK_RUN_HOST=0.0.0.0

## run it!
flask run
