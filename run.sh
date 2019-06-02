#!/bin/sh

export FLASK_APP=run.py
export FLASK_ENV=development
exec gunicorn -b 0.0.0.0:5000 run:app
