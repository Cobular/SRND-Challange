import os

from sqlalchemy import Table, Column, Integer
from sqlalchemy.orm import mapper, sessionmaker

from srndchallengepackage import db

db.Model.metadata.reflect(db.engine, extend_existing=True)
print(db.Model.__bases__)


class Registrations(db.Model):
    __table_args__ = {
        'extend_existing': True
    }

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    region_name = db.Column(db.Text, nullable=False)
    promo_code = db.Column(db.Text, nullable=False)
    ticket_type = db.Column(db.Text, nullable=False)
    ticket_cost = db.Column(db.Integer, default=0)
    registered_at = db.Column(db.Integer, nullable=False)
    checked_in_at = db.Column(db.Integer)

    def __repr__(self):
        return self.first_name


class Sponsors(db.Model):
    __table_args__ = {
        'extend_existing': True
    }

    name = db.Column(db.Text, nullable=False, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    region_name = db.Column(db.Text, nullable=False)
