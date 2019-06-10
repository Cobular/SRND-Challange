"""Directly run this file with flask run. Make this the FLASK_APP"""
from srndchallengepackage import create_app

app = create_app()

from srndchallengepackage.main.util import jinja_tools
