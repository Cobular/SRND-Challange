from flask import render_template
from sqlalchemy.sql import label
from sqlalchemy.sql.functions import sum, count

from srndchalengepackage.main import bp
import datetime as dt


@bp.route("/")
def hello_world():
    return "Hello World!"


@bp.route("/data")
def data():
    from srndchalengepackage.models import Registrations as Reg, Sponsors
    from srndchalengepackage import db

    # Some stuff that's useful in a few places:
    region_list = (
        db.session.query(Reg.region_name)
        .distinct(Reg.region_name)
        .group_by(Reg.region_name)
        .all()
    )

    # Calculate the ticket related info
    ticket_sales = (
        db.session.query(sum(Reg.ticket_cost)).scalar() * 0.01
    )  # Ticket costs in cents
    sponsor_bucks = (
        db.session.query(sum(Sponsors.amount)).scalar() * 0.01
    )  # Sponsors value is in cents
    food_costs = db.session.query(Reg).count() * 11  # Food cost = $11 per attendee
    net_costs = ticket_sales + sponsor_bucks - food_costs

    # ------------------------------------------------------------------------------------------------------------------

    # Calculate the early bird related info
    early_birds = {}
    for event in region_list:
        total_attendee_count = (
            db.session.query(Reg).filter(Reg.region_name == event[0]).count()
        )
        early_bird_count = (
            db.session.query(Reg)
            .filter(
                Reg.region_name == event[0],
                Reg.registered_at
                <= dt.datetime.fromtimestamp(1550318400) - dt.timedelta(weeks=2),
            )
            .limit(total_attendee_count * 0.4)
            .count()
        )
        early_birds[event.region_name] = (early_bird_count, total_attendee_count)
    print(early_birds)

    # ------------------------------------------------------------------------------------------------------------------

    # Calculates the promo related info
    # Returns the number of uses of each promo code
    promo_data = (
        db.session.query(Reg.promo_code, count(Reg.promo_code).label("num_uses"))
        .group_by(Reg.promo_code)
        .order_by(count(Reg.promo_code).desc())
        .all()
    )
    print(promo_data)

    # ------------------------------------------------------------------------------------------------------------------
    # Calculates attendance and registration info per region
    checked_registered_data = (
        db.session.query(
            Reg.region_name,
            count(Reg.checked_in_at).label("num_checked_in"),
            count(Reg.registered_at).label("num_registered"),
        )
        .group_by(Reg.region_name)
        .all()
    )

    checked_registered_data = (
        checked_registered_data
        + db.session.query(
            Reg.first_name,
            count(Reg.checked_in_at).label("num_checked_in"),
            count(Reg.registered_at).label("num_registered"),
        ).all()
    )

    print(checked_registered_data)

    # ------------------------------------------------------------------------------------------------------------------

    return render_template(
        "results.html",
        netcosts=net_costs,
        earlybirds=early_birds,
        promos=promo_data,
        registration_info=checked_registered_data,
    )
