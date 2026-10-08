# Clink plugins (Rares)

Five Clink Pro plugins, designed to go with the **Rares Glass** profile in [`dobrerares/clink-typing-profiles`](https://github.com/dobrerares/clink-typing-profiles). The four typing plugins install switched off; the layout plugin is on so its layout shows up.

- **Period Guard** shrinks the period key's tap area after a one-time calibration. It doesn't change how keys look or how tall they are.
- **Quiet Feedback** gives each key its own crisp, clearly felt haptic. It never plays sounds or takes over native settings.
- **Bilingual Guard** leaves Clink's autocorrect on, but blocks the corrections that tend to go wrong: links, emails, numbers, codes, ACRONYMS, Romanian hyphen forms (s-a, mi-am, într-un), case-only changes, and fixes that strip your diacritics. It also **restores Romanian diacritics** for about 120 common words that are never valid without them (rau → rău, maine → mâine, si → și, dupa → după). A Strict switch keeps every word exactly as typed.
- **Rares QWERTY** adds two layouts, both standard QWERTY with an **emoji key left and a period key right of the space bar**. **Rares QWERTY Compact** also adds its own narrow, SwiftKey-style return key. It's built the same way as Clink's official Colemak-DH plugin. Pick it in Layout → Arrangement; it installs as a normal custom layout.
- **Explicit Proofread** is an Apple Intelligence button that acts only on selected text, after you acknowledge a warning. It isn't safe to use on Romanian text.

Full phone setup: [SETUP-rares-glass.md](https://github.com/dobrerares/clink-typing-profiles/blob/main/SETUP-rares-glass.md).

## Install

In Clink, add `dobrerares/clink-typing-plugins` under repositories, then install the plugins from the plugin catalogue.

## Build and test

```sh
python3 -B tools/build-manifest.py
python3 -B -m unittest discover -s tests -v
```

CI builds the manifest, runs the tests, then publishes a permanent, content-addressed release. Any source change needs a plugin version bump so installed copies update. The desktop tests use fake Clink API builders and don't prove behaviour on a phone. This is a v0.1 phone-test release.

## Provenance

The builder is copied unchanged from https://github.com/anti-ltd/clink-plugins (SHA-256 2c740c06017fd7d22f4bbd3703bffa67b861d2f0d86ca6be97d97e534ce68921). The official release workflow is copied with an added unittest gate. The four plugins and their tests are original work. No official plugin is redistributed: install Language Flag from the official repository. This material is for Clink only and is distributed for free under the included Clink Community Assets License 1.0. No official endorsement is claimed.
