from database.connection import SessionLocal
from database.models import Match, Prediction


db = SessionLocal()

try:

    finished_matches = (
        db.query(Match)
        .filter(Match.status == "finished")
        .all()
    )

    updated = 0

    for match in finished_matches:

        predictions = (
            db.query(Prediction)
            .filter(Prediction.match_id == match.id)
            .all()
        )

        for pred in predictions:

            exact = False
            correct = False
            points = 1

            # Exact score = 6 points
            if (
                pred.predicted_home_score == match.home_score
                and
                pred.predicted_away_score == match.away_score
            ):
                points = 6
                exact = True
                correct = True

            else:

                predicted_result = (
                    pred.predicted_home_score
                    - pred.predicted_away_score
                )

                actual_result = (
                    match.home_score
                    - match.away_score
                )

                # Correct winner/draw = 4 points
                if (
                    (predicted_result > 0 and actual_result > 0)
                    or
                    (predicted_result < 0 and actual_result < 0)
                    or
                    (predicted_result == 0 and actual_result == 0)
                ):
                    points = 4
                    correct = True

            pred.points_earned = points
            pred.is_exact_score = exact
            pred.is_correct_result = correct

            updated += 1

    db.commit()

    print(f"Updated {updated} predictions.")

finally:
    db.close()