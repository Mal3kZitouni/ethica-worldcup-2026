import streamlit as st
from deep_translator import GoogleTranslator

# ----------------------------------
# Translation cache
# ----------------------------------
_translation_cache = {}

# ----------------------------------
# Manual translations
# ----------------------------------
CUSTOM_TRANSLATIONS = {
    "Group Stage": "Phase de groupes",
    "Round of 32": "1/16 de finale",
    "Round of 16": "1/8 de finale",
    "Quarter Finals": "Quarts de finale",
    "Semi Finals": "Demi-finales",
    "3rd Place Match": "Match pour la 3e place",
    "Final": "Finale",

    "Home": "Accueil",
    "Matches": "Matchs",
    "My Predictions": "Mes pronostics",
    "Tables": "Tableaux",
    "Rankings": "Classement",
    "My Profile": "Mon profil",
    "Administration": "Administration",
    "Welcome": "Bienvenue",
    "point": "point",
    "Matches Points": "Points des matchs"
}


def tr(text):
    """
    Global translation function.

    RULE:
    - Write ALL UI text in English.
    - If language = EN -> return original text.
    - If language = FR -> auto-translate to French.
    """

    if text is None:
        return ""

    text = str(text)

    lang = st.session_state.get("lang", "en")

    # English
    if lang == "en":
        return text

    # Manual translations first
    if text in CUSTOM_TRANSLATIONS:
        return CUSTOM_TRANSLATIONS[text]

    cache_key = f"{lang}:{text}"

    if cache_key in _translation_cache:
        return _translation_cache[cache_key]

    try:

        translated = GoogleTranslator(
            source="en",
            target="fr"
        ).translate(text)

        _translation_cache[cache_key] = translated

        return translated

    except Exception:

        return text