import streamlit as st
import pandas as pd

from services.table_service import get_group_tables
from services.translations import tr


def show():

    st.title(f"📊 {tr('Group Tables')}")

    tables = get_group_tables()

    # -----------------------------------
    # No data fallback
    # -----------------------------------
    if not tables:

        st.info(
            tr("No groups or matches available yet.")
        )

        return

    # -----------------------------------
    # Group selection
    # -----------------------------------
    groups = sorted(
        tables.keys()
    )

    selected_group = st.selectbox(
        tr("Select Group"),
        groups
    )

    st.subheader(
        f"{tr('Group')} {selected_group}"
    )

    df = tables[selected_group]

    # -----------------------------------
    # Optional column translations
    # -----------------------------------
    column_translations = {
        "Team": tr("Team"),
        "Played": tr("Played"),
        "Wins": tr("Wins"),
        "Draws": tr("Draws"),
        "Losses": tr("Losses"),
        "Goals For": tr("Goals For"),
        "Goals Against": tr("Goals Against"),
        "Goal Difference": tr("Goal Difference"),
        "Points": tr("Points")
    }

    df = df.rename(
        columns=column_translations
    )

    # -----------------------------------
    # Display table
    # -----------------------------------
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )