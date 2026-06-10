from database.models import Prediction


def get_prediction(
    db,
    user_id,
    match_id
):
    return (
        db.query(Prediction)
        .filter(
            Prediction.user_id == user_id,
            Prediction.match_id == match_id
        )
        .first()
    )


def create_prediction(
    db,
    prediction
):
    db.add(prediction)


def get_user_predictions(
    db,
    user_id
):
    return (
        db.query(Prediction)
        .filter(
            Prediction.user_id == user_id
        )
        .all()
    )