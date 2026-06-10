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

    col1, col2, col3, col4, col5 = st.columns(
        [1, 4, 3, 2, 2]
    )

    col1.markdown(f"**{tr('Rank')}**")
    col2.markdown(f"**{tr('User')}**")
    col3.markdown(f"**{tr('Country')}**")
    col4.markdown(f"**{tr('Points')}**")
    col5.markdown(f"**{tr('Predictions')}**")

    st.markdown("---")

    for idx, row in enumerate(
        ranking,
        start=1
    ):

        c1, c2, c3, c4, c5 = st.columns(
            [1, 4, 3, 2, 2]
        )

        if idx == 1:
            rank = "🥇"
        elif idx == 2:
            rank = "🥈"
        elif idx == 3:
            rank = "🥉"
        else:
            rank = str(idx)

        c1.write(rank)
        c2.write(row.name)
        c3.write(row.country or "-")
        c4.write(row.points)
        c5.write(row.predictions)

        st.markdown("---")