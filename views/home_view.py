import streamlit as st

from services.match_service import load_matches
from services.prediction_service import get_user_predictions
from services.ranking_service import get_ranking
from services.Chat_IA import render_chat_panel
from services.translations import tr


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
                background: linear-gradient(90deg,#4d408c,#E6BEEA);
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
                <div class="reward-title">🥅 {tr('Match Points')}</div>
                <div class="reward-line">⚽ {tr('Exact Score')}: <b>5 {tr('points')}</b></div>
                <div class="reward-line">🎯 {tr('Correct Result')}: <b>3 {tr('points')}</b></div>
                <div class="reward-line">❌ {tr('Wrong prediction')}: <b>1 {tr('pt')}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Bonus points card
        st.markdown(
            f"""
            <div class="reward-card">
                <div class="reward-title">⚽ {tr('Tournament Winner Prediction')}</div>
                <div class="reward-line">⚽ {tr('Group Stage')}: <b>15 {tr('points')}</b></div>
                <div class="reward-line">🏆 {tr('Round of 32')}: <b>12 {tr('points')}</b></div>
                <div class="reward-line">🏆 {tr('Round of 16')}: <b>10 {tr('points')}</b></div>
                <div class="reward-line">🏆 {tr('Quarter Finals')}: <b>7 {tr('points')}</b></div>
                <div class="reward-line">🏆 {tr('Semi Finals')}: <b>5 {tr('points')}</b></div>
                <div class="reward-line">🏆 {tr('Final')}: <b>3 {tr('points')}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ==================================================
        # PROFILE INFO
        # ==================================================
        col1, col2 = st.columns(2)

        with col1:
            st.info(
                f"🌍 {tr('Country')}: "
                f"{user_country if user_country else tr('Not specified')}"
            )

        with col2:
            st.info(
                f"👥 {tr('Team')}: "
                f"{user_team if user_team else 'P&A'}"
            )

        # ==================================================
        # USER STATS
        # ==================================================
        predictions = get_user_predictions(user_id)

        total_predictions = len(predictions)
        total_points = sum(p.points_earned for p in predictions)
        correct_results = sum(
            1 for p in predictions if p.is_correct_result
        )
        exact_scores = sum(
            1 for p in predictions if p.is_exact_score
        )

        st.subheader(f"📊 {tr('My Statistics')}")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(tr("Predictions"), total_predictions)
        c2.metric(tr("Points"), total_points)
        c3.metric(tr("Correct Results"), correct_results)
        c4.metric(tr("Exact Scores"), exact_scores)

        st.markdown("---")

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

                mc1, mc2 = st.columns([3, 1])

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
        st.subheader(f"🥇 {tr('Top 5 Players')}")

        top5 = ranking[:5]

        for position, player in enumerate(top5, start=1):

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
    # AI CHAT PANEL
    # ==================================================
    with col_chat:
        render_chat_panel()