import streamlit as st

from services.match_service import load_matches
from services.prediction_service import (
    get_user_predictions,
    save_prediction
)
from services.country_flags import get_flag_url
from services.translations import tr


# ----------------------
# TOURNAMENT STAGES
# ----------------------
ALL_STAGES = [
    "Group Stage",
    "Round of 32",
    "Round of 16",
    "Quarter Finals",
    "Semi Finals",
    "3rd Place Match",
    "Final"
]


# ----------------------
# STAGE STATUS
# ----------------------
def get_stage_status(matches):

    return {
        stage: any(
            m.stage == stage
            for m in matches
        )
        for stage in ALL_STAGES
    }


# ----------------------
# MAIN PAGE
# ----------------------
def show():

    st.title(f"⚽ {tr('Matches')}")

    if "prediction_success" in st.session_state:

        st.success(st.session_state["prediction_success"])
        del st.session_state["prediction_success"]

    matches = load_matches()

    if not matches:
        st.warning(tr("No matches found"))
        return

    user_id = st.session_state.get("user_id")

    user_predictions = get_user_predictions(user_id)

    predicted_match_ids = {
        str(p.match_id)
        for p in user_predictions
    }

    stage_status = get_stage_status(matches)

    # ==================================================
    # FILTERS
    # ==================================================
    st.markdown(f"### 🔍 {tr('Filters')}")

    col1, col2, col3 = st.columns(3)

    stage_options = [tr("All")] + [
        f"{'🔓' if stage_status[s] else '🔒'} {tr(s)}"
        for s in ALL_STAGES
    ]

    with col1:

        selected_stage_raw = st.selectbox(
            tr("Stage"),
            stage_options
        )

    selected_stage = (
        selected_stage_raw
        .replace("🔓 ", "")
        .replace("🔒 ", "")
    )

    stage_mapping = {
        tr(stage): stage
        for stage in ALL_STAGES
    }

    selected_stage = stage_mapping.get(
        selected_stage,
        selected_stage
    )

    dates = sorted(
        list(
            set(
                str(m.match_date).split(" ")[0]
                for m in matches
            )
        )
    )

    with col2:

        selected_date = st.selectbox(
            tr("Date"),
            [tr("All")] + dates
        )

    with col3:

        search = st.text_input(tr("Search Team"))

    # ==================================================
    # FILTER FUNCTION
    # ==================================================
    def match_filter(match):

        if (
            selected_stage != tr("All")
            and selected_stage != "All"
            and match.stage != selected_stage
        ):
            return False

        if (
            selected_date != tr("All")
            and selected_date != "All"
            and str(match.match_date).split(" ")[0]
            != selected_date
        ):
            return False

        if search:
            text = search.lower()
            if (
                text not in match.home_team.lower()
                and text not in match.away_team.lower()
            ):
                return False

        return True

    # ==================================================
    # FILTER MATCHES
    # ==================================================
    filtered_matches = []

    for match in matches:

        if not match_filter(match):
            continue

        if (
            match.home_score is not None
            and match.away_score is not None
        ):
            continue

        if str(match.id) in predicted_match_ids:
            continue

        filtered_matches.append(match)

    if not filtered_matches:

        st.success(tr("You have predicted all available matches."))
        return

    # ==================================================
    # DISPLAY MATCHES
    # ==================================================
    for match in filtered_matches:

        render_match(match, user_id)


# ----------------------
# MATCH CARD
# ----------------------
def render_match(match, user_id):

    st.markdown("---")

    try:
        formatted_date = (
            match.match_date.strftime("%Y-%m-%d %H:%M") + " GMT"
        )
    except Exception:
        formatted_date = str(match.match_date)

    # ==================================================
    # TEAMS
    # ==================================================
    col1, col2, col3 = st.columns([5, 2, 5])

    with col1:
        st.markdown(
            f"""
            <div style="text-align:center;">
                <img src="{get_flag_url(match.home_team)}" width="60">
                <h3>{match.home_team}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="text-align:center; padding-top:40px;">
                <h2>VS</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="text-align:center;">
                <img src="{get_flag_url(match.away_team)}" width="60">
                <h3>{match.away_team}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ==================================================
    # MATCH INFO
    # ==================================================
    st.markdown(
        f"""
        <div style="text-align:center; margin-top:10px; margin-bottom:15px;">
            <h4>🏆 {tr(match.stage)}</h4>
            <p>📅 {formatted_date}</p>
            <p>🏟 {match.stadium} - {match.city}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==================================================
    # PREDICTION FORM
    # ==================================================
    with st.form(key=f"prediction_form_{match.id}"):

        st.subheader(tr("Your Prediction"))

        colA, colB = st.columns(2)

        # ======================
        # HOME TEAM SCORE
        # ======================
        with colA:
            home = st.number_input(
                f"{match.home_team} {tr('Score')}",
                min_value=0,
                max_value=20,
                value=0,
                key=f"h_{match.id}"
            )

        # ======================
        # AWAY TEAM SCORE
        # ======================
        with colB:
            away = st.number_input(
                f"{match.away_team} {tr('Score')}",
                min_value=0,
                max_value=20,
                value=0,
                key=f"a_{match.id}"
            )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:

            submitted = st.form_submit_button(
                f"⚽ {tr('Make Prediction')}",
                use_container_width=True
            )

        with col_btn2:

            bet_clicked = st.form_submit_button(
                f"💰 {tr('Place a Bet')}",
                use_container_width=True
            )

        # ======================
        # SAVE PREDICTION
        # ======================
        if submitted:

            save_prediction(
                user_id,
                match.id,
                home,
                away
            )

            st.session_state["prediction_success"] = (
                f"✅ {tr('Prediction made successfully for')} "
                f"{match.home_team} vs {match.away_team}"
            )

            st.rerun()

        # ======================
        # BET WARNING (UNCHANGED)
        # ======================
        if bet_clicked:

            st.markdown("""<div>🛑 Politique de Conformité & Valeurs du Groupe P&A</div>
                            <div class="ethica-warning-body">
                    This is a non-betting prediction platform for fun, teamwork and engagement.
                    Betting or gambling is strictly prohibited.
                </div>""", unsafe_allow_html=True)