# ---
# name: Bilingual Guard
# icon: text.badge.checkmark
# summary: Lets autocorrect work, restores Romanian diacritics, protects links, codes and clitics
# version: 0.3
# author: Rares
# enabled: false
# ---

# Smart mode (default): Clink's own autocorrect runs. With Romanian + English in
# Combined mode, Clink only corrects a word that is wrong in every enabled
# language. This plugin vetoes only the corrections that typically go wrong:
# links, emails, numbers, codes, ACRONYMS, Romanian hyphen forms (s-a, mi-am,
# într-un, deployment-ul), case-only changes, and fixes that strip the
# diacritics you typed. Strict mode keeps every word exactly as typed.
#
# Restore diacritics (default on): a curated list of common Romanian words whose
# diacritic-free spelling is NOT itself a valid Romanian or English word
# (rau, maine, si, inca, dupa, fara, multumesc, ...). Typing one and pressing
# space commits the Romanian spelling. Where two spellings exist the far more
# common one wins (rau -> rău, not râu; pana -> până). Words that are valid
# without diacritics (sa, ca, la, in, tara, fata, buna, casa, masa) and anything
# that is also English (cat, tie, paste, care, are) are deliberately absent.

SUGGESTIONS = {"teh": "the", "recieve": "receive", "definately": "definitely", "multumesc": "mulțumesc"}
STRIP = {"ă": "a", "â": "a", "î": "i", "ș": "s", "ş": "s", "ț": "t", "ţ": "t",
         "Ă": "A", "Â": "A", "Î": "I", "Ș": "S", "Ş": "S", "Ț": "T", "Ţ": "T"}
MAX_LEN = 64

DIACRITICS = {
    # small words
    "si": "și", "ma": "mă", "isi": "își", "imi": "îmi", "iti": "îți", "niste": "niște",
    "asa": "așa", "cand": "când", "cate": "câte", "cati": "câți", "cativa": "câțiva",
    "cateva": "câteva", "catre": "către", "decat": "decât", "atat": "atât", "atata": "atâta",
    "incat": "încât", "intai": "întâi", "dupa": "după", "fara": "fără", "pana": "până",
    "daca": "dacă", "caci": "căci", "adica": "adică", "fiindca": "fiindcă", "totusi": "totuși",
    "insa": "însă", "inca": "încă", "intre": "între", "odata": "odată", "niciodata": "niciodată",
    "oricand": "oricând", "aceeasi": "aceeași", "acelasi": "același", "putin": "puțin",
    "rau": "rău", "usor": "ușor", "tarziu": "târziu", "incet": "încet", "acasa": "acasă",
    "inainte": "înainte", "inapoi": "înapoi", "impreuna": "împreună", "intotdeauna": "întotdeauna",
    # time
    "maine": "mâine", "poimaine": "poimâine", "astazi": "astăzi", "marti": "marți",
    "sambata": "sâmbătă", "duminica": "duminică", "saptamana": "săptămână",
    "saptamani": "săptămâni", "craciun": "crăciun",
    # numbers
    "doua": "două", "sase": "șase", "sapte": "șapte",
    # verbs
    "esti": "ești", "sunteti": "sunteți", "stiu": "știu", "stii": "știi", "stie": "știe",
    "stim": "știm", "poti": "poți", "vreti": "vreți", "facut": "făcut", "vad": "văd",
    "vazut": "văzut", "gasit": "găsit", "gasesc": "găsesc", "ramane": "rămâne", "ramas": "rămas",
    "ramai": "rămâi", "astept": "aștept", "asteapta": "așteaptă", "iesi": "ieși", "iesim": "ieșim",
    "iesit": "ieșit", "intreb": "întreb", "inteleg": "înțeleg", "intelegi": "înțelegi",
    "inteles": "înțeles", "inseamna": "înseamnă", "incep": "încep", "incepe": "începe",
    "incerc": "încerc", "incearca": "încearcă", "intalnim": "întâlnim", "intarzii": "întârzii",
    "raspund": "răspund", "cumpar": "cumpăr", "cumparat": "cumpărat", "platesc": "plătesc",
    "platit": "plătit", "mananc": "mănânc", "mancat": "mâncat", "multumesc": "mulțumesc",
    "multumim": "mulțumim",
    # nouns / other
    "multumiri": "mulțumiri", "intrebare": "întrebare", "intrebari": "întrebări",
    "raspuns": "răspuns", "intalnire": "întâlnire", "intarziere": "întârziere",
    "greseala": "greșeală", "gresit": "greșit", "mancare": "mâncare", "paine": "pâine",
    "branza": "brânză", "sanatate": "sănătate", "gand": "gând", "ganduri": "gânduri",
    "baiat": "băiat", "baiatul": "băiatul", "barbat": "bărbat", "oras": "oraș",
    "orasul": "orașul", "cumparaturi": "cumpărături", "romania": "românia",
    "romaneste": "românește", "bucuresti": "bucurești",
}
# Capitalised forms that are English names or words, so left alone when capitalised.
CAP_SKIP = {"maine", "ma", "cate", "marti", "inca"}

def initial():
    return {"on": True, "strict": False, "suggest": False, "restore": True}

def settings(state):
    return vstack([
        toggle("Protect mixed RO/EN typing", state.get("on", True), action="on"),
        toggle("Restore Romanian diacritics (rau → rău)", state.get("restore", True), action="restore"),
        toggle("Strict: never change a word", state.get("strict", False), action="strict"),
        toggle("Offer curated fixes (never automatic)", state.get("suggest", False), action="suggest"),
        text("Restore fixes about 120 common Romanian words that are never valid without diacritics (maine → mâine, si → și, dupa → după); the more common spelling wins (rau → rău). Smart mode keeps autocorrect on but blocks fixes to links, emails, numbers, codes, acronyms, s-a / mi-am style words, and fixes that remove your diacritics. Strict blocks every change."),
    ])

def on_action(action, value, state):
    if action in ["on", "strict", "suggest", "restore"]:
        state[action] = value is True
    return state

def _plain(s):
    out = ""
    for ch in s:
        out += STRIP.get(ch, ch)
    return out

def _protected(word):
    if len(word) > MAX_LEN:
        return True
    for ch in word:
        if ch.isdigit() or ch in "@/:_\\#&=?%+-.'’":
            return True
    letters = [ch for ch in word if ch.isalpha()]
    if len(letters) >= 2 and word == word.upper():
        return True
    return False

def _restore(word):
    low = word.lower()
    target = DIACRITICS.get(low)
    if target is None:
        return None
    if word == low:
        return target
    if word == low[0].upper() + low[1:] and low not in CAP_SKIP:
        return target[0].upper() + target[1:]
    return None

def correct(word, fix, state):
    # Stores nothing. Returns a word to commit, False (keep as typed) or None (let Clink decide).
    if not isinstance(state, dict) or state.get("on", True) is not True:
        if isinstance(state, dict) and state.get("on", True) is False:
            return None
        return False
    if state.get("strict", False) is True:
        return False
    if not isinstance(word, str) or word == "":
        return False
    if _protected(word):
        return False
    if state.get("restore", True) is True:
        restored = _restore(word)
        if restored is not None:
            return restored
    if isinstance(fix, str) and fix != word:
        if fix.lower() == word.lower():
            return False
        if _plain(word) != word and fix == _plain(word):
            return False
    return None

def suggestions(word, state):
    if not isinstance(state, dict) or state.get("on", True) is False or state.get("suggest", False) is not True:
        return []
    if not isinstance(word, str) or not word.isalpha() or word != word.lower():
        return []
    replacement = SUGGESTIONS.get(word)
    return [replacement] if replacement else []
