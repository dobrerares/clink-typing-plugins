# ---
# name: Quiet Feedback
# icon: hand.tap
# summary: Crisp, clearly felt letters; firmer space, solid return, sharp delete; no sounds
# version: 0.2
# author: Rares
# enabled: false
# ---

import math

def initial():
    return {"on": True, "strength": 1.0}

def strength(state):
    value = state.get("strength", 1.0)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 1.0
    if not math.isfinite(value):
        return 1.0
    return max(0.5, min(1.4, value))

def settings(state):
    return section("haptics.feel", [
        toggle("Quiet per-key feedback", state.get("on", True), action="on"),
        slider("Feedback strength", strength(state), min=0.5, max=1.4, step=0.05, key="strength"),
        text("No sound commands or geometry changes. Cursor feedback remains the profile's native feedback."),
    ], title="Quiet Feedback")

def on_action(action, value, state):
    if action == "on":
        state["on"] = value is True
    elif action == "strength":
        state["strength"] = value
        state["strength"] = strength(state)
    return state

def haptics(state):
    if state.get("on", True) is False:
        return {}
    gain = strength(state)
    # v0.2: crisper and clearly felt (v0.1 was too faint). Tight, high-sharpness
    # taps for letters like a premium keyboard click; space a rounder thump;
    # return the most solid; delete short and sharp. Max 0.7 * 1.4 < 1.0.
    return {
        "letters": feel("light", intensity=0.5 * gain, sharpness=0.72),
        "keys": feel("light", intensity=0.46 * gain, sharpness=0.7),
        "space": feel("medium", intensity=0.62 * gain, sharpness=0.58),
        "return": feel("rigid", intensity=0.7 * gain, sharpness=0.85),
        "delete": feel("light", intensity=0.42 * gain, sharpness=0.82),
        "shift": feel("light", intensity=0.46 * gain, sharpness=0.7),
    }
