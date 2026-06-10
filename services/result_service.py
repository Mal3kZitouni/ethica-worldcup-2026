from database.connection import SessionLocal
from database.models import Match, Prediction


def save_match_result(
    match_id,
    home_score,
    away_score
):

    db = SessionLocal()

    try:

        match = (
            db.query(Match)
            .filter(Match.id == match_id)
            .first()
        )

        if not match:
            return

        match.home_score = home_score
        match.away_score = away_score
        match.status = "finished"

        predictions = (
            db.query(Prediction)
            .filter(
                Prediction.match_id == match_id
            )
            .all()
        )

        for pred in predictions:

            points = 0
            exact = False
            correct = False

            # Exact score
            if (
                pred.predicted_home_score == home_score
                and
                pred.predicted_away_score == away_score
            ):
                points = 3
                exact = True
                correct = True

            else:

                predicted_result = (
                    pred.predicted_home_score
                    -
                    pred.predicted_away_score
                )

                actual_result = (
                    home_score
                    -
                    away_score
                )

                if (
                    (predicted_result > 0 and actual_result > 0)
                    or
                    (predicted_result < 0 and actual_result < 0)
                    or
                    (predicted_result == 0 and actual_result == 0)
                ):
                    points = 1
                    correct = True

            pred.points_earned = points
            pred.is_exact_score = exact
            pred.is_correct_result = correct

        db.commit()

    finally:
        db.close()