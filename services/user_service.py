from database.connection import SessionLocal
from database.models import User


def get_user_by_id(user_id):

    db = SessionLocal()

    try:
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    finally:
        db.close()


def update_profile(
    user_id,
    name,
    country,
    team
):

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            return

        user.name = name
        user.country = country
        user.team = team

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


from database.connection import SessionLocal
from database.models import User


def get_all_countries():

    db = SessionLocal()

    try:

        countries = (
            db.query(User.country)
            .filter(
                User.country.isnot(None),
                User.country != "",
                User.role != "admin"
            )
            .distinct()
            .order_by(User.country)
            .all()
        )

        return [c[0] for c in countries]

    finally:
        db.close()