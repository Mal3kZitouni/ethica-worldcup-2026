from database.connection import SessionLocal
from database.models import User, Prediction
from sqlalchemy import func


def get_ranking(country=None):

    db = SessionLocal()

    try:

        query = (
            db.query(
                User.name,
                User.country,
                func.coalesce(
                    func.sum(Prediction.points_earned),
                    0
                ).label("points"),
                func.count(
                    Prediction.id
                ).label("predictions")
            )
            .outerjoin(
                Prediction,
                User.id == Prediction.user_id
            )
            .filter(
                User.role != "admin"
            )
        )

        if country and country != "All Countries":
            query = query.filter(
                User.country == country
            )

        ranking = (
            query
            .group_by(
                User.id,
                User.name,
                User.country
            )
            .order_by(
                func.coalesce(
                    func.sum(
                        Prediction.points_earned
                    ),
                    0
                ).desc(),
                func.count(
                    Prediction.id
                ).desc()
            )
            .all()
        )

        return ranking

    finally:
        db.close()