import pandas as pd

from database.connection import SessionLocal
from database.models import Match

from repositories.match_repository import (
    get_match_by_teams_and_date,
    create_match
)


def import_matches(csv_path: str):

    df = pd.read_csv(csv_path)

    db = SessionLocal()

    inserted = 0
    skipped = 0

    try:

        for _, row in df.iterrows():

            match_datetime = pd.to_datetime(
                f"{row['date']} {row['time_et']}"
            )

            existing_match = get_match_by_teams_and_date(
                db=db,
                home_team=row["team_a"],
                away_team=row["team_b"],
                match_date=match_datetime
            )

            if existing_match:
                skipped += 1
                continue

            match = Match(
                stage=row["stage"],
                group_name=row["group"]
                if pd.notna(row["group"])
                else None,
                match_date=match_datetime,
                home_team=row["team_a"],
                away_team=row["team_b"],
                stadium=row["venue"],
                city=row["city"],
                status="scheduled",
                created_by_admin=False
            )

            create_match(
                db=db,
                match=match
            )

            inserted += 1

        db.commit()

        print(f"Imported: {inserted}")
        print(f"Skipped: {skipped}")

    except Exception as e:

        db.rollback()

        print(f"ERROR: {e}")

    finally:

        db.close()