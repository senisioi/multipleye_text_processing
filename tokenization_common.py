import unicodedata

HAUSA_STOP = set([
    "a","amma","ba","ban","ce","cikin","da","don","ga","in","ina","ita","ji","ka","ko",
    "kuma","lokacin","ma","mai","na","ne","ni","sai","shi","su","suka","sun","ta",
    "tafi","take","tana","wani","wannan","wata","ya","yake","yana","yi","za"
])

GALLICIAN_STOP = set(["a", "alí", "ao", "aos", "aquel", "aquela", "aquelas", "aqueles", "aquilo", "aquí", "as", "así", "aínda", "ben", "cando", "che", "co", "coa", "coas", "comigo", "con", "connosco", "contigo", "convosco", "cos", "cun", "cunha", "cunhas", "cuns", "da", "dalgunha", "dalgunhas", "dalgún", "dalgúns", "das", "de", "del", "dela", "delas", "deles", "desde", "deste", "do", "dos", "dun", "dunha", "dunhas", "duns", "e", "el", "ela", "elas", "eles", "en", "era", "eran", "esa", "esas", "ese", "eses", "esta", "estaba", "estar", "este", "estes", "estiven", "estou", "está", "están", "eu", "facer", "foi", "foron", "fun", "había", "hai", "iso", "isto", "la", "las", "lle", "lles", "lo", "los", "mais", "me", "meu", "meus", "min", "miña", "miñas", "moi", "na", "nas", "neste", "nin", "no", "non", "nos", "nosa", "nosas", "noso", "nosos", "nun", "nunha", "nunhas", "nuns", "nós", "o", "os", "ou", "para", "pero", "pode", "pois", "pola", "polas", "polo", "polos", "por", "que", "se", "senón", "ser", "seu", "seus", "sexa", "sido", "sobre", "súa", "súas", "tamén", "tan", "te", "ten", "ter", "teu", "teus", "teñen", "teño", "ti", "tido", "tiven", "tiña", "túa", "túas", "un", "unha", "unhas", "uns", "vos", "vosa", "vosas", "voso", "vosos", "vós", "á", "é", "ó", "ós"])


def isalpha_inclusive(s: str) -> bool:
    if not s:
        return False
    saw_base = False
    for ch in unicodedata.normalize("NFC", s):
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat == "Nd":
            saw_base = True
            continue
        if cat in ("Mn", "Mc", "Me"):
            if not saw_base:
                return False
            continue
        return False
    return True

def is_punct(token: str) -> bool:
    token = token.strip()
    if not token:
        return False
    return all(unicodedata.category(ch).startswith("P") for ch in token)

def eos_row(lang_name, lang_code, stimulus_name, page):
    return {
        "id": "_",
        "language": lang_name,
        "language_code": lang_code,
        "stimulus_name": stimulus_name,
        "page": page,
        "token": "<eos>",
        "is_alpha": False,
        "is_stop": False,
        "is_punct": False,
        "lemma": "",
        "upos": "",
        "xpos": "",
        "feats": "",
        "head": "",
        "deprel": "",
        "deps": "",
        "misc": ""
    }