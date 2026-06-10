from database.connection import SessionLocal
from database.models import WinnerPrediction


def get_winner_prediction(user_id):

    db = SessionLocal()

    try:
        return (
            db.query(WinnerPrediction)
            .filter(
                WinnerPrediction.user_id == user_id
            )
            .first()
        )

    finally:
        db.close()


def save_winner_prediction(
    user_id,
    predicted_winner,
    prediction_stage
):

    db = SessionLocal()

    try:

        existing = (
            db.query(WinnerPrediction)
            .filter(
                WinnerPrediction.user_id == user_id
            )
            .first()
        )

        # LOCK FOREVER
        if existing:
            return False

        db.add(
            WinnerPrediction(
                user_id=user_id,
                predicted_winner=predicted_winner,
                prediction_stage=prediction_stage
            )
        )

        db.commit()

        return True

    except Exception as e:

        db.rollback()
        raise e

    finally:

        db.close()