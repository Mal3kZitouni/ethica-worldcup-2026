from database.connection import SessionLocal

from repositories.match_repository import (
    get_all_matches
)


def load_matches():

    db = SessionLocal()

    try:

        return get_all_matches(db)

    finally:

        db.close()