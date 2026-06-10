import streamlit as st

from services.auth_service_auth import authenticate_user
from services.register_service import register_user
from services.translations import tr

from utils.session import initialize_session

from views import (
    home_view,
    matches_vieww,
    predictions_view,
    tables_view,
    rankings_view,
    profile_view,
    admin_view
)

# ----------------------
# INIT SESSION
# ----------------------
st.set_page_config(
    page_title="Ethica World Cup 2026",
    page_icon="🏆",
    layout="wide"
)

initialize_session()

if "lang" not in st.session_state:
    st.session_state.lang = "fr"

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

st.markdown("""
<style>

:root{
    --ethica-primary:#8D40DA;
    --ethica-secondary:#E6BEEA;
}

/* Buttons */
.stButton > button {
    background-color:#8D40DA;
    color:white;
    border:none;
    border-radius:12px;
    font-weight:600;
    transition:all .25s ease;
}

.stButton > button:hover{
    background-color:#7A32C7;
    transform:translateY(-2px);
}

/* Tabs */
button[data-baseweb="tab"]{
    color:#8D40DA;
}

/* Success boxes */
.stSuccess{
    border-left:5px solid #8D40DA;
}

/* Links */
a{
    color:#8D40DA !important;
}

/* Radio labels */
div[role="radiogroup"] label{
    color:#8D40DA;
}

/* Language selector */
div[role="radiogroup"]{
    gap:8px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# GLOBAL LANGUAGE SELECTOR
# ==================================================
with st.sidebar:

    st.markdown(f"##### 🌐 {tr('Application Language')}")

    selected_lang = st.radio(
        "",
        ["🇫🇷 Français", "🇬🇧 English"],
        horizontal=True,
        label_visibility="collapsed",
        index=0 if st.session_state.lang == "fr" else 1,
        key="language_selector"
    )

    new_lang = (
        "fr"
        if "Français" in selected_lang
        else "en"
    )

    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()

    st.markdown("---")

# ==================================================
# LOGIN / SIGNUP
# ==================================================
if not st.session_state.get("authenticated", False):

    login_tab, signup_tab = st.tabs(
        [
            f"🔑 {tr('Login')}",
            f"📝 {tr('Sign Up')}"
        ]
    )

    # ==================================================
    # LOGIN
    # ==================================================
    with login_tab:

        st.title(
            f"🏆 {tr('Ethica World Cup 2026 Predictions')}"
        )

        email = st.text_input(
            tr("Email Address"),
            key="login_email"
        )

        password = st.text_input(
            tr("Password"),
            type="password",
            key="login_password"
        )

        if st.button(
            tr("Login"),
            key="login_button"
        ):

            user = authenticate_user(
                email,
                password
            )

            if user:

                st.session_state.authenticated = True
                st.session_state.user_id = str(user.id)
                st.session_state.user_name = user.name
                st.session_state.user_email = user.email
                st.session_state.country = user.country
                st.session_state.team = user.team
                st.session_state.role = user.role

                st.rerun()

            else:
                st.error(
                    tr("Invalid credentials")
                )

    # ==================================================
    # SIGNUP
    # ==================================================
    with signup_tab:

        st.title(
            f"📝 {tr('Create Account')}"
        )

        name = st.text_input(
            tr("Full Name")
        )

        from utils.countries import COUNTRIES

        country = st.selectbox(
            tr("Country"),
            COUNTRIES
        )

        team = st.text_input(
            tr("Team"),
            value="Ethica",
            disabled=True
        )

        email_signup = st.text_input(
            tr("Email Address"),
            key="signup_email"
        )

        password_signup = st.text_input(
            tr("Password"),
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            tr("Confirm Password"),
            type="password"
        )

        if st.button(
            tr("Create Account"),
            key="signup_button"
        ):

            if not name:

                st.error(
                    tr("Name is required")
                )

            elif not email_signup:

                st.error(
                    tr("Email is required")
                )

            elif not email_signup.lower().endswith("@groupe-ethica.com"):

                st.error(
                    "Only @groupe-ethica.com email addresses are allowed."
                )

            elif password_signup != confirm_password:

                st.error(
                    tr("Passwords do not match")
                )

            else:

                success, message = register_user(
                    name=name,
                    email=email_signup,
                    password=password_signup,
                    country=country,
                    team=team
                )

                if success:
                    st.success(
                        tr("Account created successfully. You can now login.")
                    )
                else:
                    st.error(message)

# ==================================================
# MAIN APP
# ==================================================
else:

    with st.sidebar:

        st.image(
            "assets/ethica_logo.png",
            width=180
        )

        st.markdown("---")

        menu_items = {
            tr("Home"): "Home",
            tr("Matches"): "Matches",
            tr("My Predictions"): "Predictions",
            tr("Tables"): "Tables",
            tr("Rankings"): "Rankings",
            tr("My Profile"): "Profile"
        }

        menu_labels = list(
            menu_items.keys()
        )

        if st.session_state.get("role") == "admin":

            admin_label = tr("Administration")

            menu_items[
                admin_label
            ] = "Admin"

            menu_labels.append(
                admin_label
            )

        reverse_menu = {
            v: k
            for k, v in menu_items.items()
        }

        default_index = 0

        if (
            st.session_state.current_page
            in reverse_menu
        ):

            selected_label = reverse_menu[
                st.session_state.current_page
            ]

            if selected_label in menu_labels:

                default_index = (
                    menu_labels.index(
                        selected_label
                    )
                )

        page_selected = st.radio(
            tr("Navigation"),
            menu_labels,
            index=default_index
        )

        page = menu_items[
            page_selected
        ]

        st.session_state.current_page = page

        st.markdown("---")

        if st.button(
            tr("Logout")
        ):
            st.session_state.clear()
            st.rerun()

    # ==================================================
    # ROUTING
    # ==================================================
    if page == "Home":
        home_view.show()

    elif page == "Matches":
        matches_vieww.show()

    elif page == "Predictions":
        predictions_view.show()

    elif page == "Tables":
        tables_view.show()

    elif page == "Rankings":
        rankings_view.show()

    elif page == "Profile":
        profile_view.show()

    elif page == "Admin":
        admin_view.show()