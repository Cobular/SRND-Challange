from random import sample

from flask import render_template
from sqlalchemy.sql import label
from sqlalchemy.sql.functions import sum, count

from srndchallengepackage.main import bp
import datetime as dt


@bp.route("/")
def data():
    from srndchallengepackage.models import Registrations as Reg, Sponsors
    from srndchallengepackage import db

    # Some stuff that's useful in a few places:
    region_list = (
        db.session.query(Reg.region_name)
            .order_by(Reg.region_name.asc())
            .distinct(Reg.region_name)
            .group_by(Reg.region_name)
            .all()
    )

    print(dir(Sponsors))

    # Calculate the ticket related info
    ticket_sales = (
            db.session.query(sum(Reg.ticket_cost)).scalar() / 100
    )  # Ticket costs in cents
    sponsor_bucks = (
            db.session.query(sum(Sponsors.amount)).scalar() / 100
    )  # Sponsors value is in cents
    food_costs = db.session.query(Reg).count() * 11  # Food cost = $11 per attendee
    net_costs = ticket_sales + sponsor_bucks - food_costs
    all_cost_data = [ticket_sales, sponsor_bucks, food_costs, net_costs]

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
    early_birds = sorted(early_birds.items())
    print(early_birds)

    # ------------------------------------------------------------------------------------------------------------------

    # Calculates the promo related info
    # Returns the number of uses of each promo code
    promo_data = (
        db.session.query(
            Reg.promo_code, count(1).label("num_uses")
        )  # Returns code:count, does count none
            .group_by(Reg.promo_code)
            .order_by(
            count(Reg.promo_code).desc()
        )  # does NOT count none here, so none will always be last
            .all()
    )

    full_colors = [
        "#3F97CC", "#48DCC6", "#FF686B", "#C71585",
        "#E6E6E6", "#4169E1", "#F7464A", "#46BFBD",
        "#FDB45C", "#FEDCBA", "#ABCDEF", "#DDDDDD",
        "#ABCABC", "#FF4500", "#FEDCBA", "#46BFBD", ]

    promo_code_names = []
    promo_code_uses = []
    for element in promo_data:
        promo_code_names.append(str(element.promo_code))
        promo_code_uses.append(int(element.num_uses))
    selected_colors = full_colors[0:len(promo_code_names) - 1]
    promo_chart_data = [promo_code_names, selected_colors, promo_code_uses]
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
        Reg.first_name,  # Need to get the text "Overall" into this field
        count(Reg.checked_in_at).label("num_checked_in"),
        count(Reg.registered_at).label("num_registered"),
    ).all()
    )

    print(checked_registered_data)

    # ------------------------------------------------------------------------------------------------------------------

    return render_template(
        "results.html",
        cost_data=all_cost_data,
        earlybirds=early_birds,
        promos=promo_data,
        registration_info=checked_registered_data,
        promo_chart_data=promo_chart_data,
    )
