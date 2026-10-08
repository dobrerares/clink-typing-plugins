# ---
# name: Period Guard (offline prototype)
# icon: scope
# summary: Calibrated period-only hitbox guard; off by default
# version: 0.1-local
# author: Local prototype
# enabled: false
# ---

import math

# These are calibration candidates, NOT claimed documented key spellings.
# Never accept letters/keys fallbacks, arbitrary text, or another special key.
PERIOD_CANDIDATES = [".", "period", "dot"]


def initial():
    return {"on": False, "scale": 0.92, "offset": 0.0,
            "space_on": False, "space_scale": 1.02,
            "_field": "unknown", "_armed": False, "_candidate": "",
            "_ready": False, "_period": "",
            "_status": "not_calibrated"}


def bounded(value, low, high, default):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    if isinstance(value, float) and not math.isfinite(value):
        return default
    return max(low, min(high, value))


def clean(state):
    # Only our configuration and bounded runtime markers survive a hook return.
    out = initial()
    if not isinstance(state, dict):
        return out
    out["on"] = state.get("on") is True
    out["space_on"] = state.get("space_on") is True
    out["scale"] = bounded(state.get("scale"), 0.88, 1.0, 0.92)
    out["offset"] = bounded(state.get("offset"), -0.06, 0.06, 0.0)
    out["space_scale"] = bounded(state.get("space_scale"), 1.0, 1.04, 1.02)
    if state.get("_field") in ["default", "email", "url", "number", "phone", "search", "password"]:
        out["_field"] = state["_field"]
    # No free-form key IDs, text, coordinates, samples or tap history.
    if out["on"]:
        out["_armed"] = state.get("_armed") is True
        if state.get("_candidate") in PERIOD_CANDIDATES:
            out["_candidate"] = state["_candidate"]
            out["_ready"] = state.get("_ready") is True
        if state.get("_period") in PERIOD_CANDIDATES:
            out["_period"] = state["_period"]
        if state.get("_status") in ["armed", "tap_again", "ready", "confirmed", "unsupported"]:
            out["_status"] = state["_status"]
    return out


def forget(state):
    state["_armed"] = False
    state["_candidate"] = ""
    state["_ready"] = False
    state["_period"] = ""
    state["_status"] = "not_calibrated"
    return state


def settings(state):
    s = clean(state)
    return section("keys.hitboxes", [
        toggle("Period Guard (off by default)", s["on"], action="on"),
        slider(s["scale"], min=0.88, max=1.0, step=0.01,
               label="Period target scale", action="scale"),
        slider(s["offset"], min=-0.06, max=0.06, step=0.01,
               label="Horizontal offset (positive = right)", action="offset"),
        toggle("Also expand space target (experimental)", s["space_on"], action="space_on"),
        slider(s["space_scale"], min=1.0, max=1.04, step=0.01,
               label="Space target scale", action="space_scale"),
        text("Calibration: " + s["_status"] + "; confirmed ID: " + s["_period"]),
        text("In a disposable ordinary text field, arm then tap the visible period twice. Confirm only if both taps typed periods. Coordinates and text are never read or saved."),
        button("Arm period calibration", action="arm"),
        button("Confirm those were period taps", action="confirm"),
        button("Cancel / forget calibration", action="forget"),
        text("Unknown and non-default fields are excluded. Other planes/languages clear calibration. No broad special-key fallback. Unsupported IDs fail closed."),
    ], title="Period Guard - local prototype")


def on_action(action, value, state):
    s = clean(state)
    if action == "on":
        s["on"] = value is True
        if not s["on"]:
            forget(s)
    elif action == "space_on":
        s["space_on"] = value is True
    elif action == "scale":
        s["scale"] = bounded(value, 0.88, 1.0, 0.92)
    elif action == "offset":
        s["offset"] = bounded(value, -0.06, 0.06, 0.0)
    elif action == "space_scale":
        s["space_scale"] = bounded(value, 1.0, 1.04, 1.02)
    elif action == "arm" and s["on"]:
        forget(s)
        s["_armed"] = True
        s["_status"] = "armed"
    elif action == "confirm" and s["on"] and s["_ready"]:
        s["_period"] = s["_candidate"]
        s["_candidate"] = ""
        s["_armed"] = False
        s["_ready"] = False
        s["_status"] = "confirmed"
    elif action == "forget":
        forget(s)
    return s


def on_open(state):
    s = clean(state)
    # Wait for an actual field-kind notification; never assume prose.
    s["_field"] = "unknown"
    return s


def on_close(state):
    s = clean(state)
    s["_field"] = "unknown"
    # Runtime-only ID markers may be shared with settings. They are not saved.
    return s


def on_field(kind, state):
    s = clean(state)
    s["_field"] = kind if kind in ["default", "email", "url", "number", "phone", "search", "password"] else "unknown"
    if s["_field"] != "default":
        s["_armed"] = False
        s["_candidate"] = ""
        s["_ready"] = False
        s["_status"] = "confirmed" if s["_period"] else "not_calibrated"
    return s


def on_language(code, state):
    return forget(clean(state))


def events(state):
    return ["plane"]


def on_event(name, info, state):
    s = clean(state)
    if name == "plane":
        # Plane strings are not relied on for activation. Any notification
        # invalidates calibration, even an unknown/malformed plane payload.
        forget(s)
    return s


def on_touch(key, x, y, state):
    s = clean(state)
    if not s["on"] or not s["_armed"] or s["_field"] != "default":
        return s
    if key not in PERIOD_CANDIDATES:
        forget(s)
        s["_status"] = "unsupported"
    elif s["_candidate"] == key:
        s["_ready"] = True
        s["_armed"] = False
        s["_status"] = "ready"
    else:
        s["_candidate"] = key
        s["_ready"] = False
        s["_status"] = "tap_again"
    return s


def hitboxes(state):
    s = clean(state)
    if not s["on"] or s["_field"] != "default" or not s["_period"]:
        return {}
    out = {}
    if s["scale"] != 1.0 or s["offset"] != 0.0:
        out[s["_period"]] = hitbox(scale=s["scale"], x=s["offset"], y=0.0)
    if s["space_on"] and s["space_scale"] != 1.0:
        out["space"] = hitbox(scale=s["space_scale"], x=0.0, y=0.0)
    return out
