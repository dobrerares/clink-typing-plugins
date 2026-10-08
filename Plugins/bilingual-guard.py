# ---
# name: Bilingual Guard
# icon: text.badge.checkmark
# summary: Lets autocorrect work, but protects links, codes, Romanian clitics and diacritics
# version: 0.2
# author: Rares
# enabled: false
# ---

# Smart mode (default): Clink's own autocorrect runs. With Romanian + English in
# Combined mode, Clink only corrects a word that is wrong in every enabled
# language. This plugin vetoes only the corrections that typically go wrong:
# links, emails, numbers, codes, ACRONYMS, Romanian hyphen forms (s-a, mi-am,
# într-un, deployment-ul), case-only changes, and fixes that strip the
# diacritics you typed. Strict mode keeps every word exactly as typed.

SUGGESTIONS = {"teh": "the", "recieve": "receive", "definately": "definitely", "multumesc": "mulțumesc"}
STRIP = {"ă": "a", "â": "a", "î": "i", "ș": "s", "ş": "s", "ț": "t", "ţ": "t",
         "Ă": "A", "Â": "A", "Î": "I", "Ș": "S", "Ş": "S", "Ț": "T", "Ţ": "T"}
MAX_LEN = 64

def initial():
    return {"on": True, "strict": False, "suggest": False}

def settings(state):
    return vstack([
        toggle("Protect mixed RO/EN typing", state.get("on", True), action="on"),
        toggle("Strict: never change a word", state.get("strict", False), action="strict"),
        toggle("Offer curated fixes (never automatic)", state.get("suggest", False), action="suggest"),
        text("Smart mode keeps autocorrect on but blocks fixes to links, emails, numbers, codes, acronyms, s-a / mi-am / într-un style words, and fixes that remove your diacritics. Strict blocks every correction."),
    ])

def on_action(action, value, state):
    if action in ["on", "strict", "suggest"]:
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

def correct(word, fix, state):
    # Stores nothing. Returns False (keep as typed) or None (let Clink decide).
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
