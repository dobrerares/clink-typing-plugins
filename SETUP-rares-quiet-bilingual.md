Rares Quiet Bilingual — phone test setup, not yet published

Status
  Local profile and four packaged plugins are built and desktop-tested.
  No GitHub publication, phone changes, purchases or permission changes have occurred.
  The local plugin manifest deliberately has UNPUBLISHED-LOCAL-ONLY URLs. They are not installation links.
  Phone/PyMini validation is still required. “Latest App Store build” is the user's report, not an exact independently verified version.

Design
  Start with Clink Default. Normal Default letter-key height/width/spacing are intentionally inherited, never enlarged. Compact number row is added above it.
  The profile configures values supported by official Fastest/Smoothest profiles or the supplied exported-profile history. It does not invent language, plugin or theme IDs.
  Choices outside the profile go in the checklist below. Completing the profile import alone does NOT complete the setup.
  Setting labels can vary between released app builds; the linked official pages are the reference. If a named control is absent, record the actual version and missing control rather than guessing a substitute.

Choices and reasons
  Layout: QWERTY for both languages, ordinary full-width keyboard; split and one-handed off — stable thumb geometry without taller keys.
  Height/spacing: Clink Default — rejects the previous tall-key approach; no custom keyHeight is included.
  Number row: on, 0.8-height compact row — numbers stay accessible without making letter keys taller.
  Look: built-in Native paired theme, Automatic appearance on — clean contrast in light/dark, no extra theme repository or decorative distractions.
  Key material/font: Native defaults, no custom font, no custom drawn keys — legibility and platform familiarity.
  Popups: floating popups on; native letter size; long-press accent choices on; long-press preview glyphs off — readable touch feedback and Romanian diacritics without clutter.
  Motion: instant key response, no bloom enlargement, damped short response, no lean/morph or swipe trail; animated backgrounds/effects off — calm, direct motion instead of rubbery keys.
  Haptics: gentle letters (0.28), distinct space (0.42), crisp return (0.40), light delete (0.20), soft shift (0.24), other keys (0.25), with adjustable gain — confirmation varies by key's purpose rather than becoming noisy.
  Cursor: native spacebar trackpad, 200 ms activation delay, cursor activation haptic on — deliberate editing without competing spacebar language flicks.
  Sounds: OFF explicitly in profile AND confirm Sound & Haptics off — hard requirement; no sound packs, sound-volume plugin or audio commands.
  Suggestions: on; normal three choices; Fit more suggestions off, Scrollable suggestions off; language button on — readable manual alternatives, no crowded strip.
  Autocorrect: native Autocorrect off; Bilingual Guard on — the strict preset preserves RO/EN words rather than automatically rewriting them.
  Curated fixes: optional suggestions-only switch, off initially — offers the/the typo repair and a few corrections only after opt-in, never commits them on Space.
  Languages: official Romanian plus English (UK), Combined Language Mode, both resources fully downloaded — Clink documents checking all enabled dictionaries together, without per-sentence language switching. UK is a design choice, not a claim about the user's preference.
  Punctuation: preceding-space cleanup on; auto punctuation, Space after punctuation and Double-space period OFF — avoids added punctuation/spacing and ambiguous apostrophe repairs while chasing period mis-hits.
  Capitalization/quotes: Auto-capitalize and Smart quotes off — literal mixed text/code stays unchanged; Shift and apostrophes remain manual.
  Return to letters: on — number/symbol entry returns to prose without a new language-changing gesture.
  Swipe typing: OFF initially; Multi-word swipe and Two-thumb word composition off — swipe recognition can choose a different word before the correction hook runs, so it cannot share the strict typed-word preservation claim.
  Predictive Flick and additional letter-key editing gestures: off — avoids accidental word acceptance and conflicts with later swipe testing.
  Swipe delete: off if the build exposes the native switch; native tap/hold Delete stays — prevents an accidental whole-word deletion.
  Language gestures: don't install Language Switcher; use the language button when layout switching is wanted. Native Return-up language switching can remain where Clink does not expose a disable control — Combined mode handles word recognition regardless; do not pretend an unverified gesture toggle exists.
  Official plugin: Language Flag — visible active-layout cue only; does NOT indicate that only that language's dictionary is running. Do not add Language Text/emoji badge plugins simultaneously (exclusive badge slot).
  Adaptive Hitbox: deliberately NOT enabled with Period Guard — two hitbox providers could compete; no verified overlap/merge policy or device test yet.
  Other official plugins: Heavy Space/Haptic Strength, Shorthand, Switch Volume, animations and editing/swipe plugins stay disabled — avoids overlapping haptics, first-answer correction hooks, audio and unwanted replacements.
  AI: explicit Proofread selection top-bar button, Apple Intelligence provider — no automatic AI request, no typing-triggered action, no gesture surprises.
  Privacy: analytics and clipboard-history capture off; no cloud provider, third-party API, dictation service or custom replacements added — minimizes capabilities beyond this keyboard setup. Existing saved data is NOT deleted.

Installation checklist — after publication approval and verified release URLs
  1. Acquire/activate Clink Pro yourself. In Clink, select Clink Default, then install/apply Rares Quiet Bilingual from dobrerares/clink-typing-profiles. Do not apply an older Anti-Period profile. Check Sounds OFF immediately and normal key height.
  2. Home > Themes: choose Native and Automatic appearance. Home > Languages: enable Romanian and English (UK), set both arrangements to QWERTY, choose Combined Language Mode and wait for both official language resources to finish downloading. No eo workaround or replacement language pack is needed for this first test.
  3. Home > Suggestions / Corrections / Automation: apply the switches listed above, especially Autocorrect OFF, suggestions ON, Auto punctuation OFF and Double-space period OFF. Do not add or delete replacements/custom words. If existing system or app replacements are active, test them separately: the correction-hook tests are not proof that every native replacement subsystem is disabled.
  4. Home > Gestures / Layout / Keys: apply the listed choices, especially swipe typing OFF, spacebar cursor, full-width QWERTY and floating popups/accents. In Layout > Top bar retain Suggestions, the language button and Tools; add Proofread selection once its plugin is installed. Other configurable bar buttons remain off for a compact strip.
  5. Add the proposed dobrerares/clink-typing-plugins repository in Clink's community repository management, then install Bilingual Guard, Quiet Feedback, Period Guard and Explicit Proofread. All four packages install disabled intentionally. Enable Bilingual Guard and Quiet Feedback first, checking their internal switches. Leave curated suggestions off for the initial mixed-text test.
  6. Install/enable Language Flag from the official Plugins repository. Leave the competing plugins listed above disabled. If another correct() plugin is enabled, Bilingual Guard is not guaranteed to answer first; disable the competitor before testing.
  7. Permissions are your choice, not changes made by this build. Per-key haptics on iOS and AI may need Full Access. The plugins expose native permission prompts (Typing data for correction/selected-text hooks); read each prompt. No new plugin declares network hosts or reads clipboard history. Do not grant all permissions indiscriminately. If a required grant is refused, the affected feature stays unverified/unavailable.
  8. Period Guard: enable the installed plugin and its own switch. In a disposable ordinary text field, arm calibration, tap the visible period twice, then confirm ONLY if both taps typed periods. Start at scale 0.92, zero offset and space expansion OFF. If calibration reports unsupported or never receives a normal field notification, leave it off and report that instead of forcing a broad special-key fallback. Language/layout-plane changes clear calibration deliberately; recalibrate for a changed layout. Returning to settings may affect hook notifications and must be tested on the actual phone. Small offset away from space is a later explicit experiment, not a default assumption about layout side.
  9. Home > Integrations > Apple Intelligence: choose this provider, confirm native readiness and any required native consent. Enable Explicit Proofread; read and acknowledge its warning. Add Proofread selection under Layout > Top bar. Select a short ENGLISH-ONLY passage in the receiving app before tapping. With no nonblank selection, the plugin refuses to send an AI request. Native iOS selection comes from the host app, not a plugin-created selection.
 10. After the test succeeds, save/export a NEW named profile/backup of this completed phone setup. That captures your finished baseline; it is not a request to recover the lost old export. Keep Default available as rollback. To undo a plugin, switch it off; no plugin changes or claims native settings.

Mixed-text and AI limits
  Clink's official Languages guide documents all-language spell checking and correction only if a word is wrong in every enabled language. This is useful but isn't a verified “never makes a false correction” guarantee for jargon, rare words or typos.
  Our mixed-safe hook returns False (keep word as typed) for each space-ended word; it does not choose an English or Romanian replacement. Native corrections and automatic punctuation are also switched off in the guide. Suggestions remain available for manual acceptance. This deliberately sacrifices unattended typo fixing.
  Scope: desktop tests exercise the hook with mixed sentences, URLs/email, decimals, versions, abbreviations, contractions and diacritics. They do NOT prove every phone input subsystem (swipe, Return, host-app replacements or another plugin) is covered.
  Apple Intelligence's inspected supported-language list does not include Romanian. A mixed RO/EN selection may be rejected or may be rewritten/normalized incorrectly; the exact outcome is NOT tested. ai_tools uses Clink's selected provider and replaces the selected passage. The button checks selection and warning acknowledgment, not linguistic correctness. Use English-only selections or a disposable copy of mixed text; do not expect Romanian-safe proofreading. Turning Bilingual Guard on does NOT make AI output bilingual-safe.

Phone acceptance test — never test on an important unsent message
  A. In a disposable Notes/message draft, confirm no sound on letters, Space, Delete, Return and Shift; key height remains Default; verify haptic differences and cursor activation.
  B. Type each sentence with Space after each word and compare literal words:
       Ne vedem after the meeting și discutăm deployment-ul.
       I can send raportul mâine, please review când ai timp.
       Am făcut push pe branch, but tests încă fail.
       The actual plan e să mai verificăm feedback-ul.
       Sorry, sunt late; ajung în 10 minutes.
     Also test care, actual, data, fata/fată, s-a, mi-am, într-un, API, https://example.com, a@b.ro, 3.14 and v1.2.3.
     Expected: no automatic word replacement. Accepting a suggestion is an explicit edit. Test Return/Go as well as Space. Report any native/system replacement separately.
  C. Alternate normal Space and intentional period taps before/after calibration in a disposable draft. Compare misses, not merely whether a hitbox table exists. Confirm intentional periods still work. Test URL/email fields (guard should be inactive), language/layout switching and keyboard reopen. A new field notification is required; do not assume open-hook event order.
  D. Verify Proofread with no selection sends no action; verify one selected English passage once. Keep a copy first because AI replaces the selection. Romanian/mixed proofreading remains experimental and is NOT an acceptance criterion for this English-only button.
  E. Optional later swipe experiment: only after A–D, enable single-word swipe, keep multi-word/two-thumb off and delete-whole-swiped-word off, then test the same bilingual vocabulary. Turn it back off if recognition changes language unexpectedly. This mode no longer has the strict literal typed-word guarantee.

Exactly what publication approval would cover
  Existing target: dobrerares/clink-typing-profiles, main/public release.
    Add Profiles/rares-quiet-bilingual.clinkprofile and the setup guide; publish the prepared immutable content-addressed profile workflow/validator/test changes and regenerated manifest. Existing six profiles are unchanged and remain in the catalogue; only Rares Quiet Bilingual is recommended here. Existing releases are not deleted or rewritten.
  Proposed new target: dobrerares/clink-typing-plugins, PUBLIC repository, main/public release.
    Four source files and four generated .clinkplugin assets: period-guard, quiet-feedback, bilingual-guard, explicit-proofread; content-addressed manifest; unchanged official builder; release workflow with tests before publishing; tests, guide and provenance/license notices. Version 0.1 is a phone-test release, not a device-validated production claim (Period Guard retains prototype label/version 0.1-local).
  No other repository cleanup/deletion, custom language-pack/model publication, model-training CI, purchases, account permission changes or cloud provider connection is included.
  Approval must come from the user; Atlas relaying this proposal is not approval. After approval, verify actual remote targets, publish, read back/download exact assets and verify hashes before giving installation links.

Sources checked
  https://www.anti.ltd/docs/clink/languages
  https://www.anti.ltd/docs/clink/typing
  https://www.anti.ltd/docs/clink/gestures
  https://www.anti.ltd/docs/clink/look
  https://www.anti.ltd/docs/clink/ai
  https://www.anti.ltd/docs/clink/reference/plugins
  Local upstream/clink-profiles/Profiles/fastest.clinkprofile and smoothest.clinkprofile; supplied anti-period-current.clinkprofile history for export field names.
  Local upstream/clink-plugins/README.md, PROMPT.md, VERIFY.md, Plugins/heavy-space.py and language-flag.py, tools/build-manifest.py.
  /home/rdobre/projects/clink/analysis-model-and-ai.md — .mlmodelc feasibility and unresolved autocorrect influence; no custom model is included.
