import streamlit as st
from utils.countries import COUNTRIES

from services.user_service import (
    get_user_by_id,
    update_profile
)
from services.translations import tr


def show():

    st.title(f"👤 {tr('Profile')}")

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.warning(
            tr("Please login first")
        )

        return

    user = get_user_by_id(user_id)

    if not user:

        st.error(
            tr("User not found")
        )

        return

    st.subheader(
        tr("Personal Information")
    )

    # ----------------------
    # EDITABLE FIELDS
    # ----------------------
    name = st.text_input(
        tr("Name"),
        value=user.name or ""
    )

    current_country = (
        COUNTRIES.index(user.country)
        if user.country in COUNTRIES
        else 0
    )

    country = st.selectbox(
        tr("Country"),
        COUNTRIES,
        index=current_country
    )
    # ----------------------
    # READ ONLY FIELDS
    # ----------------------
    st.text_input(
        tr("Team"),
        value=user.team or "",
        disabled=True
    )

    st.text_input(
        tr("Email"),
        value=user.email,
        disabled=True
    )

    st.text_input(
        tr("Role"),
        value=user.role,
        disabled=True
    )

    # Keep original team value
    team = user.team

    # ----------------------
    # SAVE
    # ----------------------
    if st.button(
        f"💾 {tr('Save Changes')}"
    ):

        update_profile(
            user_id=user.id,
            name=name,
            country=country,
            team=team
        )

        # Update session
        st.session_state.user_name = name
        st.session_state.country = country

        st.success(
            tr("Profile updated successfully!")
        )

        st.rerun()