from database.models import Match


def get_match_by_teams_and_date(
    db,
    home_team,
    away_team,
    match_date
):
    return (
        db.query(Match)
        .filter(
            Match.home_team == home_team,
            Match.away_team == away_team,
            Match.match_date == match_date
        )
        .first()
    )


def create_match(
    db,
    match
):
    db.add(match)


def get_all_matches(db):

    return (
        db.query(Match)
        .order_by(
            Match.match_date.asc()
        )
        .all()
    )


def get_match_by_id(
    db,
    match_id
):
    return (
        db.query(Match)
        .filter(
            Match.id == match_id
        )
        .first()
    )