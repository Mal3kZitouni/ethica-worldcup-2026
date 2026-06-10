import streamlit as st


def require_login():

    if not st.session_state.get(
        "authenticated",
        False
    ):
        st.warning(
            "Please login first."
        )
        st.stop()


def require_admin():

    require_login()

    if st.session_state.get("role") != "admin":
        st.error(
            "Administrator access required."
        )
        st.stop()