# ---
# name: Bilingual Guard
# icon: text.badge.checkmark
# summary: Preserve mixed Romanian/English words; curated fixes are suggestions only
# version: 0.1
# author: Rares
# enabled: false
# ---

SUGGESTIONS = {"teh": "the", "recieve": "receive", "definately": "definitely", "multumesc": "mulțumesc"}

def initial():
    return {"on": True, "suggest": False}

def settings(state):
    return vstack([
        toggle("Preserve mixed RO/EN words", state.get("on", True), action="on"),
        toggle("Offer curated fixes (never automatic)", state.get("suggest", False), action="suggest"),
        text("Safe mode prevents native automatic word replacement. Native suggestions remain available to choose manually. Turning it off restores Clink's normal corrections."),
    ])

def on_action(action, value, state):
    if action in ["on", "suggest"]:
        state[action] = value is True
    return state

def correct(word, fix, state):
    # No word, context, language or correction is stored. Never change a word.
    if state.get("on", True) is not False:
        return False
    return None

def suggestions(word, state):
    if state.get("on", True) is False or state.get("suggest", False) is not True:
        return []
    if not isinstance(word, str) or not word.isalpha() or word != word.lower():
        return []
    replacement = SUGGESTIONS.get(word)
    return [replacement] if replacement else []
