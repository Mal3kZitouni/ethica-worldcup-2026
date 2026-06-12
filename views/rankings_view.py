import streamlit as st

from services.ranking_service import get_ranking
from services.user_service import get_all_countries
from services.translations import tr


def show():

    st.title(f"🏆 {tr('Rankings')}")

    countries = get_all_countries()

    selected_country = st.selectbox(
        f"🌍 {tr('Filter by Country')}",
        [tr("All Countries")] + countries
    )

    ranking = get_ranking(
        None if selected_country == tr("All Countries")
        else selected_country
    )

    if not ranking:

        st.info(
            tr("No ranking data available.")
        )

        return

    # ==========================================
    # HEADER
    # ==========================================
    st.markdown(
        f"""
        <div style="
            display:grid;
            grid-template-columns:1fr 4fr 3fr 2fr 2fr;
            background:#F8F9FC;
            padding:12px;
            border-radius:10px;
            font-weight:700;
            margin-bottom:10px;
            border:1px solid #EAEAEA;
            text-align:center;
            align-items:center;
        ">
            <div>{tr('Rank')}</div>
            <div>{tr('User')}</div>
            <div>{tr('Country')}</div>
            <div>{tr('Points')}</div>
            <div>{tr('Predictions')}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==========================================
    # ROWS
    # ==========================================
    for idx, row in enumerate(ranking, start=1):

        if idx == 1:
            bg = "rgba(255, 215, 0, 0.30)"
            border = "#f6d109"
            rank = "🥇"

        elif idx == 2:
            bg = "rgba(160, 160, 160, 0.30)"
            border = "#A0A0A0"
            rank = "🥈"

        elif idx == 3:
            bg = "rgba(205, 127, 50, 0.30)"
            border = "#d9893a"
            rank = "🥉"

        else:
            bg = "#FFFFFF"
            border = "#EFEFEF"
            rank = str(idx)

        st.markdown(
            f"""
            <div style="
                background:{bg};
                border-left:5px solid {border};
                border-radius:10px;
                padding:12px;
                margin-bottom:8px;
                border:1px solid #F1F1F1;
            ">
                <div style="
                    display:grid;
                    grid-template-columns:1fr 4fr 3fr 2fr 2fr;
                    align-items:center;
                    text-align:center;
                ">
                    <div><b>{rank}</b></div>
                    <div>{row.name}</div>
                    <div>{row.country or '-'}</div>
                    <div><b>{row.points}</b></div>
                    <div>{row.predictions}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )