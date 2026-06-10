from database.connection import SessionLocal
from database.models import Match


def create_match(
    stage,
    home_team,
    away_team,
    match_date,
    stadium,
    city
):

    db = SessionLocal()

    try:

        match = Match(
            stage=stage,
            home_team=home_team,
            away_team=away_team,
            match_date=match_date,
            stadium=stadium,
            city=city,
            status="scheduled",
            created_by_admin=True
        )

        db.add(match)

        db.commit()

    finally:
        db.close()