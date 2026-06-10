import streamlit as st
from datetime import datetime, timezone

from services.match_service import load_matches
from services.prediction_service import (
    get_user_predictions,
    save_prediction
)
from services.winner_prediction_service import (
    save_winner_prediction,
    get_winner_prediction
)
from services.translations import tr
from utils.qualified_teams import QUALIFIED_TEAMS

# ----------------------
# MATCH STARTED ?
# ----------------------
def has_started(match_date):

    if match_date.tzinfo is None:
        match_date = match_date.replace(
            tzinfo=timezone.utc
        )

    return datetime.now(timezone.utc) >= match_date


# ----------------------
# MAIN PAGE
# ----------------------
def show():
    user_id = st.session_state.get("user_id")


    st.title(f"📝 {tr('My Predictions')}")

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning(
            tr("Please login to view your predictions")
        )
        return

    # ==================================================
    # TOURNAMENT WINNER PREDICTION
    # ==================================================

    from utils.tournament_stage import (
        get_active_prediction_stage
    )

    st.markdown(
        f"## 🏆 {tr('World Cup Champion Prediction')}"
    )

    active_stage = get_active_prediction_stage()

    bonus_points = {
        "Group Stage": 15,
        "Round of 32": 12,
        "Round of 16": 10,
        "Quarter Finals": 7,
        "Semi Finals": 5,
        "Final": 3
    }

    current_bonus = bonus_points.get(
        active_stage,
        0
    )

    existing_winner_prediction = get_winner_prediction(
        user_id
    )

    # ==================================================
    # ALREADY PREDICTED
    # ==================================================

    if existing_winner_prediction:

        st.markdown(
            f"""
            <div style="
                background:linear-gradient(135deg,#49264F,#00003d);
                padding:30px;
                border-radius:20px;
                color:white;
                text-align:center;
                margin-bottom:20px;
                box-shadow:0 10px 30px rgba(141,64,218,0.25);
            ">
                <h2>🏆 {tr('Your Champion')}</h2>
                <h1 style="margin-top:8px;">
                    {existing_winner_prediction.predicted_winner}
                </h1>
                <p>
                    {tr('Selected during')}
                    {tr(existing_winner_prediction.prediction_stage)}
                </p>
                <p>
                    🔒 {tr('This prediction is locked and cannot be changed')}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div style="
                background:#F8F6FD;
                border:1px solid #E6D8FA;
                padding:20px;
                border-radius:18px;
                margin-bottom:20px;
            ">
                <h3 style="color:#8D40DA;margin-bottom:5px;">
                    🏆 {tr('Who will lift the trophy in 2026?')}
                </h3>
                <p style="color:#666;">
                    {tr('Choose your World Cup champion carefully. Once saved, this prediction cannot be modified.')}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"### 🌎 {tr('Select Your Champion')}"
        )

        selected_team = st.selectbox(
            tr("World Cup Champion"),
            QUALIFIED_TEAMS
        )

        if st.button(
            f"🏆 {tr('Lock My Champion')}",
            use_container_width=True
        ):

            saved = save_winner_prediction(
                user_id,
                selected_team,
                active_stage
            )

            if saved:

                st.success(
                    f"🏆 {tr('Champion locked successfully')}: {selected_team}"
                )

            else:

                st.error(
                    tr("You have already selected your champion.")
                )

            st.rerun()


    st.markdown("---")

    predictions = get_user_predictions(user_id)

    total_predictions = len(predictions)
    total_points = sum(
        p.points_earned or 0
        for p in predictions
    )

    correct_results = sum(
        1
        for p in predictions
        if p.is_correct_result
    )

    exact_scores = sum(
        1
        for p in predictions
        if p.is_exact_score
    )

    st.subheader(f"📊 {tr('My Statistics')}")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        tr("Predictions"),
        total_predictions
    )

    c2.metric(
        tr("Points"),
        total_points
    )

    c3.metric(
        tr("Correct Results"),
        correct_results
    )

    c4.metric(
        tr("Exact Scores"),
        exact_scores
    )

    st.markdown("---")

    # ==================================================
    # MATCH PREDICTIONS
    # ==================================================

    matches = load_matches()

    predictions = get_user_predictions(
        user_id
    )

    pred_map = {
        p.match_id: p
        for p in predictions
    }

    if not pred_map:

        st.info(
            tr(
                "You haven't made any match predictions yet."
            )
        )

        return

    st.success(
        f"{tr('You made')} "
        f"{len(pred_map)} "
        f"{tr('match predictions')}"
    )

    # ----------------------
    # TABLE HEADER
    # ----------------------

    header1, header2, header3, header4 = st.columns(
        [4, 2, 2, 2]
    )

    header1.markdown(
        f"**{tr('Match')}**"
    )

    header2.markdown(
        f"**{tr('Prediction')}**"
    )

    header3.markdown(
        f"**{tr('Actual Score')}**"
    )

    header4.markdown(
        f"**{tr('Status')}**"
    )

    st.markdown("---")

    # ----------------------
    # ROWS
    # ----------------------

    for match in matches:

        pred = pred_map.get(match.id)

        if not pred:
            continue

        started = has_started(
            match.match_date
        )

        row1, row2, row3, row4 = st.columns(
            [4, 2, 2, 2]
        )

        row1.write(
            f"{match.home_team} vs {match.away_team}"
        )

        row2.write(
            f"{pred.predicted_home_score} - "
            f"{pred.predicted_away_score}"
        )

        actual_home = getattr(
            match,
            "home_score",
            None
        )

        actual_away = getattr(
            match,
            "away_score",
            None
        )

        if actual_home is None or actual_away is None:
            row3.write("—")
        else:
            row3.write(
                f"{actual_home} - {actual_away}"
            )

        if started:
            row4.error(
                f"🔒 {tr('Locked')}"
            )
        else:
            row4.success(
                f"🟢 {tr('Editable')}"
            )

        if not started:

            with st.expander(
                f"{tr('Edit prediction')} - "
                f"{match.home_team} vs "
                f"{match.away_team}"
            ):

                st.markdown(
                    f"### ⚽ {match.home_team} vs {match.away_team}"
                )

                col1, col2 = st.columns(2)

                new_home = col1.number_input(
                    f"{match.home_team} {tr('Score')}",
                    min_value=0,
                    max_value=20,
                    value=int(pred.predicted_home_score),
                    key=f"edit_home_{match.id}"
                )

                new_away = col2.number_input(
                    f"{match.away_team} {tr('Score')}",
                    min_value=0,
                    max_value=20,
                    value=int(pred.predicted_away_score),
                    key=f"edit_away_{match.id}"
                )

                st.info(
                    f"{match.home_team} {new_home} - "
                    f"{new_away} {match.away_team}"
                )

                if st.button(
                    f"💾 {tr('Update Prediction')}",
                    key=f"update_{match.id}"
                ):

                    save_prediction(
                        user_id,
                        match.id,
                        new_home,
                        new_away
                    )

                    st.success(
                        tr("Prediction updated successfully!")
                    )

                    st.rerun()

        st.markdown("---")