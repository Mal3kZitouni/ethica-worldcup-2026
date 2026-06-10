import streamlit as st
from deep_translator import GoogleTranslator

# ----------------------------------
# Translation cache
# ----------------------------------
_translation_cache = {}


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

    # English = original text
    if lang == "en":
        return text

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