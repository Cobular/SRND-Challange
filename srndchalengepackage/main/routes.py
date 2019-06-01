from flask import render_template
from sqlalchemy.sql.functions import sum

from srndchalengepackage.main import bp


@bp.route('/')
def hello_world():
    return 'Hello World!'


@bp.route('/data')
def data():
    from srndchalengepackage.models import Registrations

    ticket_cost = Registrations.query(sum(Registrations.ticket_cost)).scalar()
    return render_template('results.html', netcosts=ticket_cost, earlybirds=32323, )
