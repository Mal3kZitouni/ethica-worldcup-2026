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
    page_title="P&A World Cup 2026",
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

/* Fixed sidebar width */
section[data-testid="stSidebar"] {
    width: 320px !important;
    min-width: 320px !important;
    max-width: 320px !important;
}

/* Hide resize handle */
[data-testid="stSidebarResizeHandle"] {
    display: none !important;
}

/* Prevent content shift */
section[data-testid="stSidebar"] > div {
    width: 320px !important;
}

/* Fixed sidebar width */
section[data-testid="stSidebar"] {
    width: 320px !important;
    min-width: 320px !important;
    max-width: 320px !important;
    overflow: hidden !important;
}

/* Sidebar content */
section[data-testid="stSidebar"] > div {
    width: 320px !important;
    overflow: hidden !important;
}

/* Remove scrollbar */
section[data-testid="stSidebar"] * {
    scrollbar-width: none !important;   /* Firefox */
}

section[data-testid="stSidebar"] *::-webkit-scrollbar {
    display: none !important;           /* Chrome/Edge */
}

/* Move navigation menu to the right */
div[role="radiogroup"] {
    padding-left: 20px !important;
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

        # Keep current page selected after language change
        st.session_state.navigation_radio = (
            st.session_state.get("current_page", "Home")
        )

        st.rerun()




# ==================================================
# LOGIN / SIGNUP
# ==================================================
# ==================================================
# LOGIN / SIGNUP
# ==================================================
if not st.session_state.get("authenticated", False):

    with st.sidebar:
        st.image(
            "assets/panda.png",
            width=270
        )

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
            f"🏆 {tr('P&A World Cup 2026 Predictions')}"
        )

        with st.form("login_form"):

            email = st.text_input(
                tr("Email Address"),
                key="login_email"
            )

            password = st.text_input(
                tr("Password"),
                type="password",
                key="login_password"
            )

            login_clicked = st.form_submit_button(
                tr("Login"),
                use_container_width=True
            )

        if login_clicked:

            user = authenticate_user(
                email.strip().lower(),
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

        from utils.countries import COUNTRIES

        with st.form("signup_form"):

            name = st.text_input(
                tr("Full Name")
            )

            country = st.selectbox(
                tr("Country"),
                COUNTRIES
            )

            team = st.text_input(
                tr("Team"),
                value="P&A",
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

            signup_clicked = st.form_submit_button(
                tr("Create Account"),
                use_container_width=True
            )

        if signup_clicked:

            email_signup = email_signup.strip().lower()

            if not name:

                st.error(
                    tr("Name is required")
                )

            elif not email_signup:

                st.error(
                    tr("Email is required")
                )

            elif not email_signup.endswith(
                "@groupe-ethica.com"
            ):

                st.error(
                    "Only @groupe-ethica.com email addresses are allowed."
                )

            elif password_signup != confirm_password:

                st.error(
                    tr("Passwords do not match")
                )

            else:

                success, message = register_user(
                    name=name.strip(),
                    email=email_signup,
                    password=password_signup,
                    country=country,
                    team=team
                )

                if success:

                    st.success(
                        tr("Account created successfully. You can now login.")
                    )

                    st.info(
                        tr("Please switch to the Login tab and sign in.")
                    )

                else:

                    st.error(message)

# ==================================================
# MAIN APP
# ==================================================
else:

    with st.sidebar:

        st.markdown(
            """
            <div style="text-align:center;">
            """,
            unsafe_allow_html=True
        )

        st.image(
            "assets/panda.png",
            width=270
        )
            # LOGO FOR LOGIN PAGE


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        menu_items = {
            "Home": tr("Home"),
            "Matches": tr("Matches"),
            "Predictions": tr("My Predictions"),
            "Tables": tr("Tables"),
            "Rankings": tr("Rankings"),
            "Profile": tr("My Profile")
        }

        if st.session_state.get("role") == "admin":
            menu_items["Admin"] = tr("Administration")

        pages = list(menu_items.keys())

        current_page = st.session_state.get(
            "current_page",
            "Home"
        )

        if current_page not in pages:
            current_page = "Home"

        selected_page = st.radio(
            "",
            pages,
            index=pages.index(current_page),
            format_func=lambda x: menu_items[x],
            key="navigation_radio"
        )

        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.rerun()

        page = st.session_state.current_page


        left, center, right = st.columns([1, 3, 2])

        with center:
            if st.button(
                tr("Logout"),
                use_container_width=True
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