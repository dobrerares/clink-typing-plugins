# Clink plugins (Rares)

Five Clink Pro plugins, designed to go with the **Rares Glass** profile in [`dobrerares/clink-typing-profiles`](https://github.com/dobrerares/clink-typing-profiles). The four typing plugins install switched off; the layout plugin is on so its layout shows up.

- **Period Guard** shrinks the period key's tap area after a one-time calibration. It doesn't change how keys look or how tall they are.
- **Quiet Feedback** gives each key its own crisp, clearly felt haptic. It never plays sounds or takes over native settings.
- **Bilingual Guard 1.0** is a touch-aware autocorrect for **Romanian + English** typed on QWERTY, built for Combined mode. It reads where each finger landed (`on_touch`), searches a ~8,300-word Romanian/English list for slips on any letter plus one missed, extra or swapped letter, weighs readings by the word before and the language you're writing in, and replaces a word only when the best reading clearly beats what you typed. Real words are protected by a large margin. Ambiguous Romanian forms (sa/să, ca/că, fata/față) change only with evidence from the word before. Typed diacritics are never stripped. For words outside its list it treats Clink's own dictionary as the judge, and it overrides Clink's fixes that don't match your taps. It also restores diacritics (multumesc → mulțumesc, sunt in → sunt în), splits missed spaces, completes words and predicts the next one, and learns your names, words, word pairs and where you tap each key. **Delete right after a correction** puts your word back, and Bilingual Guard won't change it again. A Strict switch keeps every word exactly as typed.
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

Bilingual Guard 1.0: the decoder design (Gaussian tap scoring, beam search, word-pair weighting, replace-by-margin) is adapted from Hex's TypingDecoder (https://github.com/anomalyco/hex, MIT, Copyright (c) 2026 Christopher Langton). It is a new PyMini implementation, not copied code. Its embedded word data (`DATA_RO`, `DATA_EN`, `PAIRS`, `ENDS`) is derived from FrequencyWords / OpenSubtitles 2018 word counts by Hermit Dave (https://github.com/hermitdave/FrequencyWords, word lists CC BY-SA 4.0) and Tatoeba sentence counts (https://tatoeba.org, CC BY 2.0 FR). Romanian spellings without diacritics were re-weighted with the Romanian Hunspell dictionary (ro_RO), which was used only at build time and isn't shipped. That derived word data is shared under CC BY-SA 4.0. No Google or Gboard model, weights or data are used. The desktop tests and the separate PyMini parity run (Clink's open-source interpreter, https://github.com/anti-ltd/PyMini) check its behaviour and its step budget; neither replaces a test on a phone.
