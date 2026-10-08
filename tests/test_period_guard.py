"""Desktop contract tests with fake Clink builders, not PyMini/device tests."""
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "Plugins/period-guard.py").read_text()


def builder(name):
    return lambda *args, **kwargs: {"builder": name, "args": args, "kwargs": kwargs}


def load():
    env = {name: builder(name) for name in ["section", "toggle", "slider", "text", "button"]}
    env["hitbox"] = lambda **kwargs: kwargs
    exec(compile(SOURCE, "period-guard.py", "exec"), env)
    return env


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.p = load()
        self.s = self.p["initial"]()

    def action(self, name, value=None):
        self.s = self.p["on_action"](name, value, self.s)

    def field(self, kind="default"):
        self.s = self.p["on_field"](kind, self.s)

    def touch(self, key=".", x=0.45, y=-0.2):
        self.s = self.p["on_touch"](key, x, y, self.s)

    def boxes(self):
        return self.p["hitboxes"](self.s)

    def calibrate(self, key="."):
        self.action("on", True)
        self.field()
        self.action("arm")
        self.touch(key)
        self.touch(key)
        self.action("confirm")

    def test_defaults_and_pack_disabled(self):
        self.assertFalse(self.s["on"])
        self.assertFalse(self.s["space_on"])
        self.assertEqual((self.s["scale"], self.s["offset"]), (0.92, 0.0))
        self.assertEqual(self.boxes(), {})
        self.assertIn("# enabled: false", SOURCE)

    def test_on_without_confirmation_is_inert(self):
        self.action("on", True)
        self.field()
        self.action("space_on", True)
        self.action("confirm")
        self.assertEqual(self.boxes(), {})

    def test_two_observations_and_explicit_confirmation(self):
        self.action("on", True)
        self.field()
        self.action("arm")
        self.touch()
        self.action("confirm")
        self.assertEqual(self.boxes(), {})
        self.touch()
        self.assertTrue(self.s["_ready"])
        self.assertEqual(self.boxes(), {})
        self.action("confirm")
        self.assertEqual(self.boxes(), {".": {"scale": 0.92, "x": 0.0, "y": 0.0}})

    def test_observed_safe_ids_not_assumed(self):
        for key in self.p["PERIOD_CANDIDATES"]:
            with self.subTest(key=key):
                self.s = self.p["initial"]()
                self.calibrate(key)
                self.assertEqual(set(self.boxes()), {key})

    def test_unsupported_ids_and_fallbacks_rejected(self):
        for key in ["keys", "letters", "space", "return", "delete", "shift", "globe", "a", "9", "private document", "", None, {}, ["."]]:
            with self.subTest(key=key):
                self.s = self.p["initial"]()
                self.action("on", True)
                self.field()
                self.action("arm")
                self.touch(key)
                self.touch(key)
                self.action("confirm")
                self.assertEqual(self.boxes(), {})
                self.assertEqual(self.s["_candidate"], "")

    def test_mismatched_observations_need_matching_repeat(self):
        self.action("on", True)
        self.field()
        self.action("arm")
        self.touch(".")
        self.touch("period")
        self.action("confirm")
        self.assertEqual(self.boxes(), {})
        self.touch("period")
        self.action("confirm")
        self.assertEqual(set(self.boxes()), {"period"})

    def test_off_clears_calibration_and_no_effects(self):
        self.calibrate()
        self.action("space_on", True)
        self.action("on", False)
        before = dict(self.s)
        self.touch(".")
        self.assertEqual(self.s, before)
        self.assertEqual(self.boxes(), {})
        self.action("on", True)
        self.assertEqual(self.boxes(), {})

    def test_forget_and_rearm_remove_targets(self):
        self.calibrate()
        self.action("arm")
        self.assertEqual(self.boxes(), {})
        self.action("forget")
        self.assertFalse(self.s["_armed"])

    def test_fields_excluded_unknown_fail_closed(self):
        self.calibrate()
        for kind in ["email", "url", "number", "phone", "search", "password", "other", None, {}]:
            self.field(kind)
            self.assertEqual(self.boxes(), {})
            self.action("arm")
            self.touch()
            self.touch()
            self.action("confirm")
            self.assertEqual(self.boxes(), {})
        self.field()
        self.assertEqual(self.boxes(), {})

    def test_field_switch_cancels_pending_calibration(self):
        self.action("on", True)
        self.field()
        self.action("arm")
        self.touch()
        self.touch()
        self.field("password")
        self.action("confirm")
        self.field()
        self.assertEqual(self.boxes(), {})

    def test_open_and_close_require_new_field_notification(self):
        self.calibrate()
        self.s = self.p["on_close"](self.s)
        self.assertEqual(self.boxes(), {})
        self.s = self.p["on_open"](self.s)
        self.assertEqual(self.boxes(), {})
        self.field()
        self.assertEqual(set(self.boxes()), {"."})

    def test_pending_calibration_shared_across_close_open(self):
        self.action("on", True)
        self.action("arm")
        self.s = self.p["on_open"](self.s)
        self.field()
        self.touch()
        self.touch()
        self.s = self.p["on_close"](self.s)
        self.action("confirm")
        self.s = self.p["on_open"](self.s)
        self.field()
        self.assertEqual(set(self.boxes()), {"."})

    def test_language_and_plane_invalidate_identity(self):
        self.assertEqual(self.p["events"](self.s), ["plane"])
        self.calibrate()
        self.s = self.p["on_language"]("en", self.s)
        self.assertEqual(self.boxes(), {})
        self.calibrate()
        self.s = self.p["on_event"]("plane", {"plane": "123"}, self.s)
        self.assertEqual(self.boxes(), {})

    def test_optional_space_is_modest_and_gated(self):
        self.calibrate()
        self.assertNotIn("space", self.boxes())
        self.action("space_on", True)
        self.assertEqual(self.boxes()["space"], {"scale": 1.02, "x": 0.0, "y": 0.0})
        self.action("space_scale", 999)
        self.assertEqual(self.boxes()["space"]["scale"], 1.04)
        self.assertEqual(set(self.boxes()), {".", "space"})

    def test_range_clamping_and_nonfinite_defaults(self):
        self.calibrate()
        for name, low, high, default in [("scale", 0.88, 1.0, 0.92), ("offset", -0.06, 0.06, 0.0), ("space_scale", 1.0, 1.04, 1.02)]:
            for raw, expected in [(-999, low), (999, high), (float("nan"), default), (float("inf"), default), ("bad", default), (True, default), ({}, default), (None, default)]:
                with self.subTest(name=name, raw=raw):
                    self.action(name, raw)
                    self.assertEqual(self.s[name], expected)
        self.action("scale", 1.0)
        self.action("offset", 0.0)
        self.assertEqual(self.boxes(), {})
        self.action("offset", -0.06)
        self.assertEqual(self.boxes()["."]["x"], -0.06)
        self.assertEqual(self.boxes()["."]["y"], 0.0)

    def test_malformed_saved_state_is_safe(self):
        for state in [None, [], "bad", 42, {}, {"on": "true", "_period": "."}, {"on": True, "_period": "keys", "_field": "default"}, {"on": True, "scale": {}, "offset": [], "_period": {}, "_field": []}]:
            with self.subTest(state=state):
                self.assertEqual(self.p["hitboxes"](state), {})
                self.p["settings"](state)
                out = self.p["on_action"]("unknown", None, state)
                json.dumps(out, allow_nan=False)

    def test_no_text_coordinates_or_tap_history_saved(self):
        self.calibrate()
        before = dict(self.s)
        for i in range(100):
            self.touch("private text", i, -i)
        self.assertEqual(self.s, before)
        persisted = {k: v for k, v in self.s.items() if not k.startswith("_")}
        self.assertEqual(set(persisted), {"on", "scale", "offset", "space_on", "space_scale"})
        dirty = dict(self.s, history=["secret"], before="private", x=0.5)
        out = self.p["on_action"]("unknown", None, dirty)
        self.assertNotIn("history", out)
        self.assertNotIn("before", out)
        self.assertNotIn("x", out)

    def test_settings_preserved_and_policy_surface(self):
        tree = ast.parse(SOURCE)
        calls = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
        forbidden = {"setting", "set_setting", "claim", "release", "context", "insert", "replace", "press", "haptic", "fetch", "open", "eval", "exec", "compile", "space_text", "move_cursor", "backspace", "copy"}
        self.assertFalse(calls & forbidden)
        hooks = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
        self.assertFalse(hooks & {"on_key", "on_word", "on_swipe", "space_swipes", "haptics", "layouts", "key_styles", "popups", "animations", "correct", "suggestions"})
        self.assertNotIn("__", SOURCE)
        self.assertLess(len(SOURCE.encode()), 64000)
        self.assertLess(len(SOURCE.splitlines()), 1600)
        imports = {n.name for x in tree.body if isinstance(x, ast.Import) for n in x.names}
        self.assertEqual(imports, {"math"})
        # No builder is implicitly bound to a native setting or text action.
        nodes = self.p["settings"](self.s)["args"][1]
        for node in nodes:
            self.assertFalse(set(node["kwargs"]) & {"setting", "insert", "set", "key"})
        # Exercise enabled/off paths; native APIs are deliberately absent from
        # the fake host, so any attempted native setting/effect call would fail.
        self.calibrate()
        self.action("space_on", True)
        self.boxes()
        self.action("on", False)
        self.assertEqual(self.boxes(), {})


class PackagingTests(unittest.TestCase):
    def test_official_tool_unchanged(self):
        self.assertEqual(hashlib.sha256((ROOT / "tools/build-manifest.py").read_bytes()).hexdigest(), "2c740c06017fd7d22f4bbd3703bffa67b861d2f0d86ca6be97d97e534ce68921")

    def test_manifest_matches_local_artifact(self):
        manifest = json.loads((ROOT / "manifest.json").read_text())
        self.assertEqual(len(manifest["plugins"]), 5)
        entry = next(x for x in manifest["plugins"] if x["id"] == "period-guard")
        self.assertEqual(entry["id"], "period-guard")
        data = (ROOT / "build/period-guard.clinkplugin").read_bytes()
        self.assertEqual(entry["asset"]["byteCount"], len(data))
        self.assertEqual(entry["asset"]["sha256"], hashlib.sha256(data).hexdigest())
        self.assertIn(os.environ.get("GITHUB_REPOSITORY", "UNPUBLISHED-LOCAL-ONLY"), entry["asset"]["url"])
        package = json.loads(data)
        self.assertFalse(package["enabled"])
        self.assertNotIn("network", package)
        self.assertEqual(package["source"], SOURCE.split("# ---", 2)[2].lstrip("\n"))
        self.assertEqual(package["id"], "period-guard")


if __name__ == "__main__":
    unittest.main()
