# ---
# name: Explicit Proofread
# icon: text.badge.checkmark
# summary: Proofread only explicitly selected text using Clink's selected AI provider
# version: 0.1
# author: Rares
# enabled: false
# ---

def initial():
    return {"on": True, "acknowledged": False}

def settings(state):
    return vstack([
        toggle("Show explicit Proofread button", state.get("on", True), action="on"),
        toggle("I understand provider and mixed-language risks", state.get("acknowledged", False), action="acknowledged"),
        text("Select an English passage in the host app first. Apple Intelligence does not document Romanian support; mixed text may be rewritten incorrectly. Output replaces the selected passage. This plugin does not choose a provider or grant permission."),
    ])

def on_action(action, value, state):
    if action in ["on", "acknowledged"]:
        state[action] = value is True
        return state
    if action != "proofread" or state.get("on", True) is False:
        return state
    if state.get("acknowledged", False) is not True:
        banner("Review the provider and mixed-language warning in Explicit Proofread settings first.")
        return state
    selected = context().get("selected", "")
    if not isinstance(selected, str) or not selected.strip():
        banner("Select the passage in the host app first; no AI request was sent.")
        return state
    ai_tools("proofread")
    return state

def bar_items(state):
    if state.get("on", True) is False:
        return []
    return [bar_button("proofread", "Proofread selection", icon="text.badge.checkmark", title="Proofread")]
