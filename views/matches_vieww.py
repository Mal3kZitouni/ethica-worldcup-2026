import streamlit as st

from services.match_service import load_matches
from services.prediction_service import (
    get_user_predictions,
    save_prediction
)
from services.country_flags import get_flag_url
from services.translations import tr
from datetime import datetime, timezone


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

    now = datetime.now(timezone.utc)

    for match in matches:

        if not match_filter(match):
            continue

        # Hide matches that already started
        if match.match_date <= now:
            continue

        if (
            match.home_score is not None
            and match.away_score is not None
        ):
            continue

        if str(match.id) in predicted_match_ids:
            continue

        filtered_matches.append(match)

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
            <div style="
                display:flex;
                flex-direction:column;
                align-items:center;
                justify-content:center;
            ">
                <img src="{get_flag_url(match.home_team)}"
                    style="width:120px;height:auto;">
                <div style="
                    text-align:center;
                    margin-top:10px;
                    font-size:24px;
                    font-weight:600;
                ">
                    {match.home_team}
                </div>
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
            <div style="
                display:flex;
                flex-direction:column;
                align-items:center;
                justify-content:center;
            ">
                <img src="{get_flag_url(match.away_team)}"
                    style="width:120px;height:auto;">
                <div style="
                    text-align:center;
                    margin-top:10px;
                    font-size:24px;
                    font-weight:600;
                ">
                    {match.away_team}
                </div>
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
            # Injection du style CSS de l'effet d'apparition (Warning Premium)
            st.markdown("""
                <style>
                    /* Animation d'impact et d'apparition fluide */
                    @keyframes warningPulse {
                        0% { transform: scale(0.92); opacity: 0; }
                        70% { transform: scale(1.02); }
                        100% { transform: scale(1); opacity: 1; }
                    }
                    
                    .ethica-warning-box {
                        animation: warningPulse 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
                        background: linear-gradient(135deg, #FFF5F5 0%, #FFF0F0 100%);
                        border-left: 6px solid #8D40DA; /* Rappel du violet Ethica */
                        border-right: 1px solid rgba(229, 62, 62, 0.2);
                        border-top: 1px solid rgba(229, 62, 62, 0.2);
                        border-bottom: 1px solid rgba(229, 62, 62, 0.2);
                        padding: 22px;
                        border-radius: 12px;
                        box-shadow: 0 15px 30px rgba(141, 64, 218, 0.1), 0 5px 15px rgba(229, 62, 62, 0.05);
                        margin-top: 20px;
                        color: #2D3748;
                        font-family: inherit;
                    }
                    
                    .ethica-warning-header {
                        color: #E53E3E;
                        font-size: 1.2rem;
                        font-weight: 800;
                        margin-bottom: 12px;
                        display: flex;
                        align-items: center;
                    }
                    
                    .ethica-warning-body {
                        font-size: 0.95rem;
                        line-height: 1.6;
                    }
                    
                    .ethica-highlight {
                        color: #8D40DA;
                        font-weight: 600;
                    }
                </style>
                
                <div class="ethica-warning-box">
                    <div class="ethica-warning-header">
                        🛑 Politique de Conformité & Valeurs du Performance & Analytics Team
                    </div>
                    <div class="ethica-warning-body">
                        ette plateforme est un espace exclusivement conçu pour le <b>divertissement, le team building et la convivialité</b> entre collègues. 
                        Conformément à la charte de conformité et aux politiques de responsabilité sociétale du <span class="ethica-highlight">Performance & Analytics Team</span>, 
                        les paris financiers, les jeux d'argent réel ou l'évaluation de cotes marchandes sont <b>strictement interdits</b> au sein de nos outils d'entreprise.
                        <br><br>
                        Ici, notre seule et unique monnaie est la saine compétition, le défi tactique et la fierté de voir son nom briller au sommet du classement corporate ! 
                        Merci de préserver cet esprit d'équipe et de faire rayonner les valeurs d'éthique et de bienveillance qui font la force de notre groupe. 💜
                    </div>
                </div>
            """, unsafe_allow_html=True)