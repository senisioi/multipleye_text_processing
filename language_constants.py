SPACY_LANGUAGES = [
    "ca",  # Catalan
    "zh",  # Chinese
    "hr",  # Croatian
    "da",  # Danish
    "nl",  # Dutch
    "en",  # English
    "fi",  # Finnish
    "fr",  # French
    "de",  # German
    "el",  # Greek
    "it",  # Italian
    "ja",  # Japanese
    "ko",  # Korean
    "lt",  # Lithuanian
    "mk",  # Macedonian
    "nb",  # Norwegian Bokmål
    "pl",  # Polish
    "pt",  # Portuguese
    "ro",  # Romanian
    "ru",  # Russian
    "sl",  # Slovenian
    "es",  # Spanish
    "sv",  # Swedish
    "uk",  # Ukrainian
]

CODE2LANG = {
    "ar": "Arabic",
    "ca": "Catalan",
    "cs": "Czech",
    "de": "German",
    "zd": "Swiss German",
    "gsw": "Swiss German",
    "da": "Danish",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Farsi",
    "fr": "French",
    "fi": "Finnish",
    "gl": "Galician",
    "he": "Hebrew",
    "hi": "Hindi",
    "ha": "Hausa",
    "hr": "Croatian",
    "it": "Italian",
    "kl": "Kalaallisut",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "rm": "Romansh",
    "ro": "Romanian",
    "ru": "Russian",
    "sl": "Slovenian",
    "sr": "Serbian",
    "sq": "Albanian",
    "sv": "Swedish",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "yue": "Cantonese",
    "yu": "Cantonese",
    "zh": "Mandarin",
}

LANGUAGES = list(CODE2LANG.keys())


################

LANG_COLORS = {
    # --- Germanic ---
    "en": "#F43F5E",
    "de": "#F43F5E",
    #"gsw": "#F43F5E",
    "zd": "#F43F5E",
    "nl": "#F43F5E",
    "da": "#F43F5E",
    "sv": "#F43F5E",
    "no": "#F43F5E",

    # --- Basque ---
    "eu": "#6366F1",

    # --- Romance ---
    "ca": "#F59E0B",
    "es": "#F59E0B",
    "pt": "#F59E0B",
    "it": "#F59E0B",
    "fr": "#F59E0B",
    "rm": "#F59E0B",
    "ro": "#F59E0B",
    "gl": "#F59E0B",

    # --- Slavic ---
    "sl": "#13501B",
    "hr": "#13501B",
    "sr": "#13501B",
    "mk": "#13501B",
    "pl": "#13501B",
    "cs": "#13501B",
    "uk": "#13501B",
    "ru": "#13501B",

    # --- Baltic ---
    "lt": "#C084FC",
    "lv": "#C084FC",

    # --- Finnic ---
    "et": "#00B050",
    "fi": "#00B050",

    # --- Albanian ---
    "sq": "#0D9488",

    # --- Greek ---
    "el": "#3B82F6",

    # --- Turkic ---
    "tr": "#F97316",

    # --- Semitic ---
    "ar": "#F87171",
    "he": "#F87171",

    # --- Chadic ---
    "ha": "#4206EC",

    # --- Indo-Iranian ---
    "hi": "#C220AB",
    "ur": "#C220AB",
    "fa": "#C220AB",

    # --- Sinitic ---
    "zh": "#0F9ED5",
    #"yue": "#0F9ED5",
    "yu": "#0F9ED5",

    # --- Eskimo–Aleut ---
    "kl": "#2DD4BF",
}

LANG_ORDER = [lang for lang in list(LANG_COLORS.keys())]
