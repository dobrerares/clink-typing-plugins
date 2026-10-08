# Rares Quiet Bilingual plugins — unpublished phone-test candidate

Four focused, opt-in Clink Pro plugins. Each package installs disabled.

- Period Guard: calibrated period-only hitboxes, no visual/height changes; off and inert until confirmed.
- Quiet Feedback: gentle per-key haptics; no native setting claims or sounds.
- Bilingual Guard: preserve space-ended RO/EN words. Optional curated fixes are manual suggestions, never automatic replacements.
- Explicit Proofread: selected text only, explicit button and warning acknowledgment. Not a Romanian-safe AI guarantee.

Read SETUP-rares-quiet-bilingual.md for the whole setup and phone acceptance tests. The profile is in the separate clink-typing-profiles repository. These desktop tests use fake Clink API builders; no PyMini or phone runtime is included or claimed.

Local build and test:

    GITHUB_REPOSITORY=UNPUBLISHED-LOCAL-ONLY/clink-typing-plugins python3 -B tools/build-manifest.py
    python3 -B -m unittest discover -s tests -v

The placeholder manifest is not installable. Do not publish or run the release workflow before explicit user approval. On approved GitHub CI, GITHUB_REPOSITORY identifies the real repository and assets use permanent content-addressed release URLs. The workflow builds and tests before publishing a draft release. Source changes require a plugin version bump for future installed updates.

Provenance and material changes:

The builder is copied unchanged from https://github.com/anti-ltd/clink-plugins (SHA-256 2c740c06017fd7d22f4bbd3703bffa67b861d2f0d86ca6be97d97e534ce68921). The official release workflow is copied with an added unittest gate. The APIs, Heavy Space example and plugin contracts informed our implementation; all four custom plugins and tests are local additions. No official plugin is redistributed here: install Language Flag from the official repository. This material is for Clink only and distributed without paid access under the included Clink Community Assets License 1.0. No official endorsement is claimed.
