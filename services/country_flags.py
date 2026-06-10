TEAM_CODES = {
    "Algeria": "dz",
    "Argentina": "ar",
    "Australia": "au",
    "Austria": "at",
    "Belgium": "be",
    "Bosnia and Herzegovina": "ba",
    "Brazil": "br",
    "Cabo Verde": "cv",
    "Cape Verde": "cv",  # fallback spelling
    "Canada": "ca",
    "Colombia": "co",
    "Congo DR": "cd",
    "DR Congo": "cd",
    "Croatia": "hr",
    "Curaçao": "cw",
    "Curacao": "cw",
    "Czechia": "cz",
    "Czech Republic": "cz",
    "Côte d’Ivoire": "ci",
    "Cote d'Ivoire": "ci",
    "Ecuador": "ec",
    "Egypt": "eg",
    "England": "gb-eng",
    "France": "fr",
    "Germany": "de",
    "Ghana": "gh",
    "Haiti": "ht",
    "Iran": "ir",
    "Iraq": "iq",
    "Japan": "jp",
    "Jordan": "jo",
    "Korea Republic": "kr",
    "South Korea": "kr",
    "Mexico": "mx",
    "Morocco": "ma",
    "Netherlands": "nl",
    "Holland": "nl",
    "New Zealand": "nz",
    "Norway": "no",
    "Panama": "pa",
    "Paraguay": "py",
    "Portugal": "pt",
    "Qatar": "qa",
    "Saudi Arabia": "sa",
    "Scotland": "gb-sct",
    "Senegal": "sn",
    "South Africa": "za",
    "Spain": "es",
    "Sweden": "se",
    "Switzerland": "ch",
    "Tunisia": "tn",
    "Türkiye": "tr",
    "Turkey": "tr",
    "United States": "us",
    "USA": "us",
    "Uruguay": "uy",
    "Uzbekistan": "uz",
}


def get_flag_url(team_name: str) -> str:
    """
    Returns a real flag image URL from flagcdn.
    Safe for production use.
    """

    if not team_name:
        return "https://placehold.co/80x60?text=?"

    code = TEAM_CODES.get(team_name.strip())

    if not code:
        return "https://placehold.co/80x60?text=?"

    return f"https://flagcdn.com/w160/{code}.png"