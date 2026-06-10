import streamlit as st


def initialize_session():

    defaults = {
        "authenticated": False,
        "user_id": None,
        "user_name": None,
        "user_email": None,
        "role": None
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value