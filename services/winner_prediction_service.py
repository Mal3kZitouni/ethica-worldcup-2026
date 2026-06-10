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


BONUS_POINTS = {
    "Group Stage": 15,
    "Round of 32": 12,
    "Round of 16": 10,
    "Quarter Finals": 7,
    "Semi Finals": 5,
    "Final": 3
}


def award_champion_bonus(actual_champion):

    db = SessionLocal()

    try:

        predictions = (
            db.query(WinnerPrediction)
            .all()
        )

        awarded_count = 0

        for prediction in predictions:

            if prediction.bonus_awarded:
                continue

            if (
                prediction.predicted_winner
                != actual_champion
            ):
                continue

            prediction.bonus_points = BONUS_POINTS.get(
                prediction.prediction_stage,
                0
            )

            prediction.bonus_awarded = True

            awarded_count += 1

        db.commit()

        return awarded_count

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()