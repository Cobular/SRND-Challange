import datetime

from flask import render_template
from sqlalchemy.sql.functions import sum

from srndchalengepackage.main import bp


@bp.route('/')
def hello_world():
    return 'Hello World!'


@bp.route('/data')
def data():
    from srndchalengepackage.models import Registrations, Sponsors
    from srndchalengepackage import db

    # Calculate the ticket related info
    ticket_sales = db.session.query(sum(Registrations.ticket_cost)).scalar() * 0.01  # Ticket costs in cents
    sponsor_bucks = db.session.query(sum(Sponsors.amount)).scalar() * 0.01  # Sponsors value is in cents
    food_costs = db.session.query(Registrations).count() * 11  # Food cost = $11 per attendee
    net_costs = ticket_sales + sponsor_bucks - food_costs

    # Calculate the early bird related info
    early_birds = {}
    for event in db.session.query(Registrations.region_name).distinct(Registrations.region_name).group_by(
            Registrations.region_name).all():
        total_attendee_count = db.session.query(Registrations).count()
        print(total_attendee_count)
        early_bird_count = db.session.query(Registrations).limit(total_attendee_count * 0.6).count()
        print(early_bird_count)
        early_birds[event.region_name] = early_bird_count
    print(early_birds)

    # Calculates 

    return render_template('results.html', netcosts=net_costs, earlybirds=early_birds, )


# .filter(
#             Registrations.registered_at <= datetime.datetime.fromtimestamp(1550318400) - datetime.timedelta(
#                 weeks=2))

#.filter(
            # Registrations.region_name == event.region_name,
            # Registrations.registered_at <= datetime.datetime.fromtimestamp(1550318400) - datetime.timedelta(
            #     weeks=2))
