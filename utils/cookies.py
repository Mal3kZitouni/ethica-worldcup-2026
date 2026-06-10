from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix="ethica_wc_",
    password="CHANGE_THIS_TO_A_LONG_RANDOM_SECRET"
)