import os

from sqlalchemy import Table, Column, Integer
from sqlalchemy.orm import mapper, sessionmaker

from srndchallengepackage import db

db.Model.metadata.reflect(db.engine)
print(db.Model.__bases__)


class Registrations(db.Model):
    pass

    # id = db.Column(db.Integer, primary_key=True)
    # first_name = db.Column(db.Text, nullable=False)
    # last_name = db.Column(db.Text, nullable=False)
    # email = db.Column(db.Text, nullable=False)
    # region_name = db.Column(db.Text, nullable=False)
    # promo_code = db.Column(db.Text, nullable=False)
    # ticket_type = db.Column(db.Text, nullable=False)
    # ticket_cost = db.Column(db.Integer, default=0)
    # registered_at = db.Column(db.Integer, nullable=False)
    # checked_in_at = db.Column(db.Integer)

    def __repr__(self):
        return self.first_name


class Sponsors(db.Model):
    pass

    # name = db.Column(db.Text, nullable=False)
    # amount = db.Column(db.Integer, nullable=False)
    # region_name = db.Column(db.Text, nullable=False)


def load_session():
    moz_registrations = Table("moz_registrations", db.Model.metadata, autoload=True)
    mapper(Registrations, moz_registrations)

    moz_sponsors = Table("moz_sponsors", db.Model.metadata, Column("name", Integer, primary_key=True), autoload=True)
    mapper(Sponsors, moz_sponsors)

    session = sessionmaker(bind=db.engine)
    session = session()
    return session


# db.session = sessionmaker(bind=db.Model.engine)
