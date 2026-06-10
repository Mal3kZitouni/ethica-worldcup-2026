from datetime import datetime, timezone
from database.connection import SessionLocal
from database.models import Prediction


def get_user_predictions(user_id):

    db = SessionLocal()

    try:
        return db.query(Prediction).filter(
            Prediction.user_id == user_id
        ).all()

    finally:
        db.close()


def get_user_prediction(user_id, match_id):

    db = SessionLocal()

    try:
        return db.query(Prediction).filter(
            Prediction.user_id == user_id,
            Prediction.match_id == match_id
        ).first()

    finally:
        db.close()


def save_prediction(user_id, match_id, home_score, away_score):

    db = SessionLocal()

    try:
        existing = db.query(Prediction).filter(
            Prediction.user_id == user_id,
            Prediction.match_id == match_id
        ).first()

        if existing:
            existing.predicted_home_score = home_score
            existing.predicted_away_score = away_score
            existing.updated_at = datetime.now(timezone.utc)

        else:
            db.add(Prediction(
                user_id=user_id,
                match_id=match_id,
                predicted_home_score=home_score,
                predicted_away_score=away_score,
                points_earned=0
            ))

        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()