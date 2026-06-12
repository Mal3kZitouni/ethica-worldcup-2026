import streamlit as st

from services.match_service import load_matches
from services.ranking_service import get_ranking
from services.Chat_IA import render_chat_panel
from services.translations import tr
from streamlit_float import *


@st.dialog("Performance & Analytics AI", width="large")
def ai_chat_modal():
    render_chat_panel()

# ==================================================
# POINTS REWARDS CONFIG (IMPORTANT FIX)
# ==================================================
POINTS_REWARDS = [
    ("Group Stage", 15),
    ("Round of 32", 12),
    ("Round of 16", 10),
    ("Quarter Finals", 7),
    ("Semi Finals", 5),
    ("Final", 3),
]


def show():
    
    # 🔄 Force clean reload if HTML was broken before
    if "html_reset_done" not in st.session_state:
        st.session_state.html_reset_done = True
        st.cache_data.clear()
        st.rerun()


    user_id = st.session_state.get("user_id")
    user_name = st.session_state.get("user_name")
    user_country = st.session_state.get("country", "")
    user_team = st.session_state.get("team", "P&A")

    col_main, col_chat = st.columns([6.5, 3.5], gap="large")

    with col_main:

        # ==================================================
        # HERO BANNER
        # ==================================================
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(90deg,#361f4d,#6b2ea8);
                padding:25px;
                border-radius:20px;
                margin-bottom:20px;
                color:white;
            ">
            <h1>🏆 P&A World Cup 2026</h1>
            <h3>{tr("Welcome")} {user_name}</h3>
            <p>
                {tr("Predict matches")} •
                {tr("Compete with colleagues")} •
                {tr("Climb the rankings")}
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ==================================================
        # 🟣 POINTS REWARDS SECTION (IMPROVED)
        # ==================================================

        st.markdown(f"### 🏆 {tr('Points Rewards System')}")

        st.markdown(
            """
            <style>
            .reward-card {
                background: linear-gradient(135deg, #F7F3FF, #FFFFFF);
                border: 1px solid #E6D8FA;
                padding: 14px 16px;
                border-radius: 14px;
                margin-bottom: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            }

            .reward-title {
                font-weight: 600;
                color: #8D40DA;
                margin-bottom: 6px;
            }

            .reward-line {
                margin: 4px 0;
                font-size: 15px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Match points card
        st.markdown(
            f"""
            <div class="reward-card">
                <div class="reward-title">🥅 {tr('Matches Points')}</div>
                <div class="reward-line">💡 {tr('Predictions can be created or updated until the match kicks off.')}</div>
                <div class="reward-line">⚽ {tr('Exact Score')}: <b>5 {tr('points')}</b></div>
                <div class="reward-line">🎯 {tr('Correct Result')}: <b>3 {tr('points')}</b></div>
                <div class="reward-line">❌ {tr('Make a prediction')}: <b>1 {tr('point')}</b></div>
            """,
            unsafe_allow_html=True
        )

        # Bonus points card
        st.markdown(
            f"""
            <div class="reward-card">
                <div class="reward-title">⚽ {tr('Tournament Winner Prediction')}</div>
                <div class="reward-line">💡  {tr('The earlier you choose your champion, the more bonus points you can earn if your prediction is correct.')}</div>
                <div class="reward-line">🏆 {tr('Group Stage')}: <b>15 {tr('points')}</b></div>
                <div class="reward-line">🏆 {tr('Round of 32')}: <b>12 {tr('points')}</b></div>
                <div class="reward-line">🏆 {tr('Round of 16')}: <b>10 {tr('points')}</b></div>
                <div class="reward-line">🏆 {tr('Quarter Finals')}: <b>7 {tr('points')}</b></div>
                <div class="reward-line">🏆 {tr('Semi Finals')}: <b>5 {tr('points')}</b></div>
                <div class="reward-line">🏆 {tr('Final')}: <b>3 {tr('points')}</b></div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # ==================================================
        # USER RANKING
        # ==================================================
        ranking = get_ranking()
        user_rank = None

        for index, row in enumerate(ranking, start=1):
            if row.name == user_name:
                user_rank = index
                break

        if user_rank:
            st.success(f"🏅 {tr('Your Current Ranking')}: #{user_rank}")

        st.markdown("---")

        # ==================================================
        # UPCOMING MATCHES
        # ==================================================
        st.subheader(f"⚽ {tr('Upcoming Matches')}")

        matches = load_matches()
        upcoming = sorted(matches, key=lambda m: m.match_date)

        shown = 0

        for match in upcoming:

            if match.home_score is not None and match.away_score is not None:
                continue

            stadium = match.stadium or tr("TBD")
            city = match.city or tr("TBD")

            with st.container(border=True):

                mc1, mc2 = st.columns([3, 2])

                with mc1:
                    st.markdown(f"### {match.home_team} vs {match.away_team}")
                    st.caption(f"🏆 {match.stage}")

                with mc2:
                    st.write(
                        f"📅 {match.match_date.strftime('%Y-%m-%d %H:%M')} GMT"
                    )
                    st.caption(f"🏟 {stadium} - {city}")

            shown += 1

            if shown >= 3:
                break

        # ==================================================
        # TOP 5 PLAYERS
        # ==================================================
        st.subheader(f"🥇 {tr('Top 3 Players')}")

        top3 = ranking[:3]

        for position, player in enumerate(top3, start=1):

            medal = "🥇" if position == 1 else "🥈" if position == 2 else "🥉" if position == 3 else f"#{position}"

            st.write(
                f"{medal} {player.name} — {player.points} {tr('pts')}"
            )

        st.markdown("---")

        # ==================================================
        # TOURNAMENT PROGRESS
        # ==================================================
        completed = sum(
            1 for m in matches
            if m.home_score is not None and m.away_score is not None
        )

        total_matches = len(matches)

        progress = completed / total_matches if total_matches > 0 else 0

        st.subheader(f"🌍 {tr('Tournament Progress')}")
        st.progress(progress)

        st.write(f"{completed} / {total_matches} {tr('matches completed')}")
    # ==================================================
    # FLOATING AI CHAT
    # ==================================================
    st.markdown("""
    <style>

    /* FLOATING POSITION (unchanged) */
    div[data-testid="stButton"]:has(button[kind="primary"]) {
        position: fixed !important;
        top: 30% !important;
        left: 1410px !important;
        transform: translateY(-50%) !important;
        z-index: 999999 !important;
    }

    /* CIRCLE BUTTON (unchanged except icon fix) */
    div[data-testid="stButton"] button[kind="primary"] {

        width: 65px !important;
        height: 65px !important;
        min-width: 65px !important;
        max-width: 65px !important;

        border-radius: 50% !important;

        background: linear-gradient(135deg,#361f4d,#6b2ea8) !important;
        color: white !important;

        border: none !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        padding: 0 !important;

        box-shadow: 0 10px 25px rgba(0,0,0,0.25) !important;

        transition: all 0.2s ease-in-out !important;
    }

    /* 🔥 ICON FIX ONLY (makes emoji bigger visually) */
    div[data-testid="stButton"] button[kind="primary"] p {
        margin: 0 !important;
        transform: scale(2) !important;
        line-height: 1 !important;
    }

    /* HOVER (unchanged) */
    div[data-testid="stButton"] button[kind="primary"]:hover {
        transform: scale(1.09) !important;
    }
    /* HOVER TEXT   */
    div[data-testid="stButton"] button[kind="primary"]:hover::after {
        content: "P&A Assistant";
        position: absolute;
        right: 75px;
        top: 50%;
        transform: translateY(-50%);

        background: #333;
        color: white;

        padding: 6px 10px;
        border-radius: 6px;

        white-space: nowrap;
        font-size: 12px;
}

    </style>
    """, unsafe_allow_html=True)


    # FLOATING BUTTON (UNCHANGED LOGIC)
    if st.button("🤖", key="home_ai_button", type="primary"):
        ai_chat_modal()