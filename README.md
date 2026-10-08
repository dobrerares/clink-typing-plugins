# Clink plugins (Rares)

Four opt-in Clink Pro plugins, designed to go with the **Rares Glass** profile in [`dobrerares/clink-typing-profiles`](https://github.com/dobrerares/clink-typing-profiles). Each one installs switched off.

- **Period Guard** shrinks the period key's tap area after a one-time calibration. It doesn't change how keys look or how tall they are.
- **Quiet Feedback** gives each key its own gentle haptic. It never plays sounds or takes over native settings.
- **Bilingual Guard** keeps every Romanian or English word exactly as you typed it. Any curated fix appears as a suggestion; it is never applied automatically.
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
