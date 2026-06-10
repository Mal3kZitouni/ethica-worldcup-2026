WINNER_POINTS = {
    "Group Stage": 15,
    "Round of 32": 12,
    "Round of 16": 10,
    "Quarter Finals": 7,
    "Semi Finals": 5,
    "Final": 3
}

WINNER_POINTS = {
    "Group Stage": 15,
    "Round of 32": 12,
    "Round of 16": 10,
    "Quarter Finals": 7,
    "Semi Finals": 5,
    "Final": 3
}


def calculate_winner_bonus(
    predicted_winner,
    prediction_stage,
    actual_winner
):

    if predicted_winner != actual_winner:
        return 0

    return WINNER_POINTS.get(
        prediction_stage,
        0
    )