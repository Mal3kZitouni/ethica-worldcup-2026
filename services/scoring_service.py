def calculate_points(
    predicted_home,
    predicted_away,
    actual_home,
    actual_away
):
    """
    Exact score = 5 points
    Correct winner/draw = 3 points
    Wrong prediction = 0 points
    """

    # Exact score
    if (
        predicted_home == actual_home
        and predicted_away == actual_away
    ):
        return 5

    predicted_diff = predicted_home - predicted_away
    actual_diff = actual_home - actual_away

    predicted_result = (
        "home"
        if predicted_diff > 0
        else "away"
        if predicted_diff < 0
        else "draw"
    )

    actual_result = (
        "home"
        if actual_diff > 0
        else "away"
        if actual_diff < 0
        else "draw"
    )

    if predicted_result == actual_result:
        return 3

    return 0