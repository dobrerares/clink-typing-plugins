# ---
# name: Quiet Feedback
# icon: hand.tap
# summary: Gentle letters, distinct space and return, light delete; no sounds
# version: 0.1
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
    return max(0.5, min(1.2, value))

def settings(state):
    return section("haptics.feel", [
        toggle("Quiet per-key feedback", state.get("on", True), action="on"),
        slider("Feedback strength", strength(state), min=0.5, max=1.2, step=0.05, key="strength"),
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
    return {
        "letters": feel("soft", intensity=0.28 * gain, sharpness=0.45),
        "keys": feel("light", intensity=0.25 * gain, sharpness=0.5),
        "space": feel("medium", intensity=0.42 * gain, sharpness=0.55),
        "return": feel("rigid", intensity=0.4 * gain, sharpness=0.75),
        "delete": feel("light", intensity=0.2 * gain, sharpness=0.65),
        "shift": feel("soft", intensity=0.24 * gain, sharpness=0.5),
    }
