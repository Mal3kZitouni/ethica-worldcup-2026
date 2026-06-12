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
    "Matches Points": "Points des matchs",
    "Match": "Match",
    'Actual Result': 'Résultat actuel',
    'Locked': 'Verrouillé',
    'Editable': 'Modifiable',
    "Tournament Winner Prediction": "Prédiction du vainqueur du tournoi",
    "The earlier you choose your champion, the more bonus points you can earn if your prediction is correct.": "Plus vous choisissez votre champion tôt, plus vous pouvez gagner de points bonus si votre prédiction est correcte.",
    "Your Current Ranking": "Votre classement actuel",
    "Please login to view your predictions": "Veuillez vous connecter pour voir vos pronostics",
    "Access denied": "Accès refusé",
    "Prediction": "Prédiction",
    "Add Match": "Ajouter un match",
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