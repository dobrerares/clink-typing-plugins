"""Offline hook tests: stubs do NOT validate PyMini/iOS execution."""
import ast
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
IDS = {'period-guard', 'quiet-feedback', 'bilingual-guard', 'explicit-proofread', 'rares-qwerty'}

def load(name):
    calls = []
    env = {}
    def builder(name):
        return lambda *args, **kwargs: {'kind': name, 'args': args, 'kwargs': kwargs}
    for key in ['section', 'vstack', 'toggle', 'slider', 'text', 'button', 'bar_button', 'layout', 'layout_key']:
        env[key] = builder(key)
    env['feel'] = builder('feel')
    env['hitbox'] = builder('hitbox')
    env['context'] = lambda: {'selected': ''}
    env['ai_tools'] = lambda action: calls.append(('ai', action))
    env['banner'] = lambda value: calls.append(('banner', value))
    exec(compile((ROOT/'Plugins'/f'{name}.py').read_text(), name, 'exec'), env)
    return env, calls

class BilingualEngineTests(unittest.TestCase):
    """Bilingual Guard 1.0: spatial RO/EN autocorrect. CPython stubs; PyMini parity is checked by
    autocorrect-engine/tools/parity.py, not here."""
    def setUp(self):
        self.p, self.calls = load('bilingual-guard')
        self.s = self.p['initial']()
    def c(self, word, fix, last=None, pr=None):
        if last is not None:
            self.s['last'] = last
        if pr is not None:
            self.s['pr'] = pr
        return self.p['correct'](word, fix, self.s)
    def taps(self, word, offsets=None):
        for i, ch in enumerate(word):
            x, y = (offsets or {}).get(i, (0.0, 0.0))
            self.s = self.p['on_touch'](ch, x, y, self.s)
    def test_fixes_common_typos(self):
        for word, fix, want in [('teh', 'the', 'the'), ('recieve', 'receive', 'receive'),
                                ('meetign', 'meeting', 'meeting'), ('Teh', 'The', 'The'), ('yoy', 'toy', 'you')]:
            with self.subTest(word=word):
                self.s = self.p['initial']()
                self.assertEqual(self.c(word, fix, last='thank' if word == 'yoy' else ''), want)
    def test_touch_position_decides_between_neighbours(self):
        self.taps('gpod', {1: (-0.45, 0.0)})
        self.assertEqual(self.c('gpod', None), 'good')
    def test_overrides_a_far_fetched_clink_fix(self):
        self.assertIs(self.c('care', 'car'), False)
        self.assertIs(self.c('meeting', 'melting'), False)
        self.assertIs(self.c('deployment', 'employment'), False)
    def test_never_changes_valid_words_of_mixed_sentences(self):
        sentences = [
            'Ne vedem after the meeting și discutăm deployment-ul.',
            'I can send raportul mâine, please review când ai timp.',
            'Am făcut push pe branch, but tests încă fail.',
            'The actual plan e să mai verificăm feedback-ul.',
            'Sorry, sunt late; ajung în 10 minutes.',
        ]
        for sentence in sentences:
            for token in sentence.replace(',', ' ').replace('.', ' ').replace(';', ' ').split():
                with self.subTest(token=token):
                    out = self.c(token, None)
                    self.assertIn(out, (False, None))
    def test_never_strips_typed_diacritics_or_changes_case_only(self):
        self.assertIs(self.c('fată', 'fata'), False)
        self.assertIs(self.c('mâine', 'maine'), False)
        self.assertIs(self.c('și', 'si'), False)
        self.assertIn(self.c('iphone', 'iPhone'), (False, None))
        self.assertIs(self.c('Care', 'care'), False)
    def test_restores_unambiguous_diacritics(self):
        for word, want in [('dupa', 'după'), ('multumesc', 'mulțumesc'), ('stiu', 'știu'), ('Dupa', 'După'),
                           ('mancare', 'mâncare'), ('saptamana', 'săptămână|săptămâna')]:
            with self.subTest(word=word):
                self.assertIn(self.c(word, None, last='', pr=0.9), want.split('|'))
    def test_context_decides_ambiguous_romanian_forms(self):
        self.assertEqual(self.c('sa', None, last='vreau', pr=0.95), 'să')
        self.assertEqual(self.c('ca', None, last='cred', pr=0.95), 'că')
        self.assertIn(self.c('sa', None, last='casa', pr=0.95), (False, None))
        self.assertEqual(self.c('in', None, last='sunt', pr=0.95), 'în')
        self.assertIn(self.c('in', None, last='live', pr=0.05), (False, None))
    def test_ambiguous_forms_without_context_are_kept(self):
        for word in ['fata', 'casa', 'la', 'ca', 'masa', 'care', 'are', 'pe', 'cat']:
            with self.subTest(word=word):
                self.assertIn(self.c(word, None, last='', pr=0.5), (False, None))
    def test_restore_switch_strict_and_off(self):
        self.s = self.p['on_action']('restore', False, self.s)
        self.assertIn(self.c('dupa', None, pr=0.9), (False, None))
        self.s = self.p['on_action']('restore', True, self.s)
        self.s = self.p['on_action']('strict', True, self.s)
        for word, fix in [('teh', 'the'), ('care', 'car'), ('dupa', None)]:
            self.assertIs(self.c(word, fix), False)
        self.s = self.p['on_action']('strict', False, self.s)
        self.s = self.p['on_action']('on', False, self.s)
        for token in ['teh', 'https://example.com', 'API']:
            self.assertIsNone(self.c(token, 'wrong'))
    def test_protected_tokens_are_kept(self):
        for token in ['https://example.com', 'a@b.ro', '3.14', 'v1.2.3', 's-a', 'mi-am', 'într-un', 'deployment-ul',
                      'word.word', 'os.path', 'e.g.', 'foo_bar', '12:30', 'API', 'RO', 'NASA', 'a' * 200]:
            with self.subTest(token=token):
                self.assertIn(self.c(token, 'different'), (False, None))
                self.assertEqual(self.p['suggestions'](token, self.s), [])
    def test_bad_input_fail_safe(self):
        for token in ['', None, 12]:
            self.assertIsNone(self.c(token, 'wrong'))
        for state in [None, {'on': None}, {'on': 1}, {'on': 'false'}]:
            self.assertIsNone(self.p['correct']('care', 'wrong', state))
        broken = {'on': True, 'taps': 'x', 'touch': [1], 'pp': 5, 'words': 'y', 'last': 3, 'pr': 'z'}
        self.assertIn(self.p['correct']('teh', 'the', broken), ('the', None, False))
        self.p['suggestions']('te', broken)
        self.p['on_word']('test', broken)
        self.p['on_backspace'](broken)
    def test_delete_after_a_correction_keeps_the_word(self):
        self.assertEqual(self.c('teh', 'the'), 'the')
        self.s = self.p['on_word']('the', self.s)
        self.s = self.p['on_touch']('space', 0, 0, self.s)
        self.s = self.p['on_backspace'](self.s)
        self.assertIs(self.c('teh', 'the'), False)
        self.assertIn('teh', self.s['keep'])
    def test_two_reverts_learn_the_word(self):
        for _ in range(2):
            self.s['keep'] = {k: v for k, v in self.s['keep'].items()}
            self.p['G'].pop('skip', None)
            self.s['pend'] = ['Zdravko', 'Dravko']
            self.s = self.p['on_backspace'](self.s)
        self.assertEqual(self.s['words'].get('zdravko'), 'Zdravko')
    def test_names_typed_twice_are_learned_and_completed(self):
        for _ in range(2):
            self.s = self.p['on_word']('salut', self.s)
            self.s = self.p['on_word']('Zdravin', self.s)
        self.assertIn('Zdravin', self.p['suggestions']('zdr', self.s))
        self.assertIs(self.c('Zdravin', 'driving'), False)
    def test_next_word_predictions_learn_pairs(self):
        for word in ('good', 'morning', 'good', 'morning', 'good'):
            self.s = self.p['on_word'](word, self.s)
        self.assertEqual(self.p['suggestions']('', self.s)[0], 'morning')
        self.s['last'] = 'thank'
        self.assertIn('you', self.p['suggestions']('', self.s))
    def test_completions_use_the_word_list_and_diacritics(self):
        self.s['pr'] = 0.95
        out = self.p['suggestions']('mul', self.s)
        self.assertTrue(out)
        self.assertIn('mulțumesc', [w for w in out] + self.p['suggestions']('mult', self.s))
        self.s['pr'] = 0.05
        self.s['last'] = 'i'
        self.assertIn('want', self.p['suggestions']('wan', self.s))
        self.s = self.p['on_action']('suggest', False, self.s)
        self.assertEqual(self.p['suggestions']('wan', self.s), [])
    def test_state_stays_bounded_and_serialisable(self):
        import random
        rng = random.Random(3)
        for i in range(3000):
            w = ''.join(rng.choice('abcdefghijklmnoprstuv') for _ in range(rng.randint(2, 9)))
            if i % 7 == 0:
                w = w.capitalize()
            self.s = self.p['on_word'](w, self.s)
            self.s = self.p['on_touch'](w[0].lower(), 0.1, 0.1, self.s)
        for key, cap in [('words', 400), ('seen', 200), ('pp', 400), ('keep', 200)]:
            self.assertLessEqual(len(self.s[key]), cap)
        self.assertLessEqual(len(self.s['taps']), 48)
        self.assertLess(len(json.dumps(self.s, ensure_ascii=False)), 40000)
    def test_unknown_action_and_ui_no_effects(self):
        before = json.dumps(self.s, sort_keys=True)
        self.p['on_action']('unknown', 'text', self.s)
        self.p['settings'](self.s)
        self.assertEqual(before, json.dumps(self.s, sort_keys=True))
        self.assertEqual(self.calls, [])
    def test_missed_spaces_are_split(self):
        self.assertEqual(self.c('atthe', None, last='looked', pr=0.1), 'at the')
        self.s = self.p['initial']()
        for i, ch in enumerate('ofbthe'):
            self.s = self.p['on_touch'](ch, 0.0, 0.45 if i == 2 else 0.0, self.s)
        self.assertEqual(self.c('ofbthe', None, pr=0.1), 'of the')
    def test_clinks_own_split_is_not_blocked(self):
        self.assertIn(self.c('howbare', 'how are', pr=0.1), ('how are', None))
    def test_real_words_are_never_split(self):
        for word in ['cineva', 'into', 'anyway', 'cannot', 'deoarece', 'something', 'înapoi']:
            with self.subTest(word=word):
                self.assertIn(self.c(word, None, last=''), (False, None))
    def test_clear_forgets_learning(self):
        for word in ('good', 'morning', 'Zdravin', 'Zdravin'):
            self.s = self.p['on_word'](word, self.s)
        self.s = self.p['on_action']('clear', True, self.s)
        for key in ('words', 'seen', 'pp', 'keep', 'touch'):
            self.assertEqual(self.s[key], {})


class LayoutTests(unittest.TestCase):
    def setUp(self):
        self.env, self.calls = load('rares-qwerty')
        self.lays = {l['args'][0]: l for l in self.env['layouts']({})}
    def test_two_variants(self):
        self.assertEqual(set(self.lays), {'rares-qwerty', 'rares-qwerty-compact'})
        self.assertEqual(self.calls, [])
    def test_letters_are_plain_qwerty(self):
        for lay in self.lays.values():
            rows = lay['kwargs']['rows']
            self.assertEqual([''.join(r) for r in rows], ['qwertyuiop', 'asdfghjkl', 'zxcvbnm'])
    def test_symmetric_emoji_and_period(self):
        for lay in self.lays.values():
            (emoji,) = lay['kwargs']['left']
            period = lay['kwargs']['right'][0]
            self.assertEqual(emoji['kwargs']['action'], 'emoji')
            self.assertEqual(emoji['args'], ('\u263a\ufe0e',))  # monochrome text smiley, not colour emoji
            self.assertEqual(period['args'], ('.',))
            self.assertNotIn('action', period['kwargs'])
            self.assertEqual(emoji['kwargs']['width'], period['kwargs']['width'])
    def test_compact_has_narrow_return_and_plain_does_not(self):
        self.assertEqual(len(self.lays['rares-qwerty']['kwargs']['right']), 1)
        ret = self.lays['rares-qwerty-compact']['kwargs']['right'][1]
        self.assertEqual(ret['kwargs']['action'], 'return')
        self.assertLessEqual(ret['kwargs']['width'], 1.5)
        for lay in self.lays.values():
            self.assertLessEqual(len(lay['kwargs']['left']), 3)
            self.assertLessEqual(len(lay['kwargs']['right']), 3)

class FeedbackTests(unittest.TestCase):
    def setUp(self):
        self.p, self.calls = load('quiet-feedback')
        self.s = self.p['initial']()
    def test_deliberate_all_key_groups(self):
        table = self.p['haptics'](self.s)
        self.assertEqual(set(table), {'letters','keys','space','return','delete','shift'})
        self.assertGreater(table['space']['kwargs']['intensity'], table['letters']['kwargs']['intensity'])
        self.assertLess(table['delete']['kwargs']['intensity'], table['letters']['kwargs']['intensity'])
        self.assertGreater(table['return']['kwargs']['intensity'], table['space']['kwargs']['intensity'])
        self.assertGreaterEqual(table['letters']['kwargs']['intensity'], 0.45)  # clearly felt
        self.assertGreaterEqual(table['letters']['kwargs']['sharpness'], 0.65)  # crisp
    def test_bounds_and_bad_values(self):
        for value in [-100, 100, float('nan'), float('inf'), None, True, '1']:
            table = self.p['haptics']({'on':True,'strength':value})
            for item in table.values():
                self.assertTrue(0 <= item['kwargs']['intensity'] <= 1)
                self.assertTrue(0 <= item['kwargs']['sharpness'] <= 1)
    def test_off_has_no_table_or_commands(self):
        self.assertEqual(self.p['haptics']({'on':False}), {})
        self.assertEqual(self.calls, [])
    def test_state_and_native_settings_preserved(self):
        before = dict(self.s)
        self.p['haptics'](self.s)
        self.p['settings'](self.s)
        self.assertEqual(self.s, before)
        self.assertEqual(self.calls, [])
    def test_slider_and_unknown_actions(self):
        self.assertEqual(self.p['on_action']('strength', 9, self.s)['strength'], 1.4)
        before = dict(self.s)
        self.assertEqual(self.p['on_action']('other', None, self.s), before)

class ProofreadTests(unittest.TestCase):
    def setUp(self):
        self.p, self.calls = load('explicit-proofread')
        self.s = self.p['initial']()
    def test_warning_required(self):
        self.p['context'] = lambda: {'selected':'English text'}
        self.p['on_action']('proofread', None, self.s)
        self.assertEqual([x for x in self.calls if x[0]=='ai'], [])
    def test_no_selection_never_dispatch(self):
        self.s['acknowledged'] = True
        for selected in ['', '   ', None, 42]:
            self.p['context'] = lambda selected=selected: {'selected':selected,'before':'Visible document'}
            self.p['on_action']('proofread', None, self.s)
        self.assertEqual([x for x in self.calls if x[0]=='ai'], [])
    def test_explicit_selection_dispatches_once_no_persistent_text(self):
        self.s['acknowledged'] = True
        before = dict(self.s)
        self.p['context'] = lambda: {'selected':'Please review this passage.'}
        self.p['on_action']('proofread', None, self.s)
        self.assertEqual(self.calls, [('ai','proofread')])
        self.assertEqual(self.s, before)
    def test_mixed_selection_is_not_claimed_safe(self):
        self.s['acknowledged'] = True
        self.p['context'] = lambda: {'selected':'Please review raportul mâine.'}
        self.p['on_action']('proofread', None, self.s)
        self.assertEqual(self.calls, [('ai','proofread')])
        # Dispatch isn't a model-output guarantee; user must restrict selection.
    def test_off_unknown_settings_and_bar_no_dispatch(self):
        self.s['on'] = False
        self.assertEqual(self.p['bar_items'](self.s), [])
        for action in ['proofread','unknown']:
            self.p['on_action'](action, None, self.s)
        self.p['settings'](self.s)
        self.assertEqual(self.calls, [])
    def test_button_explicit_not_gesture(self):
        buttons = self.p['bar_items'](self.s)
        self.assertEqual(len(buttons), 1)
        self.assertEqual(buttons[0]['args'][0], 'proofread')
        for hook in ['on_key','on_word','on_swipe','on_touch','on_tick']:
            self.assertNotIn(hook, self.p)

class PolicyAndPackageTests(unittest.TestCase):
    def test_policy_all_sources(self):
        sources = list((ROOT/'Plugins').glob('*.py'))
        self.assertEqual({p.stem for p in sources}, IDS)
        for path in sources:
            source = path.read_text()
            self.assertLess(len(source.encode()), 64000)
            self.assertLess(len(source.splitlines()), 1600)
            self.assertNotIn('__', source)
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    self.assertTrue(all(x.name in {'math','random','time','json','re'} for x in node.names))
                if isinstance(node, ast.ImportFrom):
                    self.assertIn(node.module, {'math','random','time','json','re'})
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, {'open','eval','exec','compile','set_setting','claim','release','insert','delete','press','copy','paste'})
    def test_manifests_exact_count_hashes_and_default_disabled(self):
        manifest = json.loads((ROOT/'manifest.json').read_text())
        self.assertEqual({item['id'] for item in manifest['plugins']}, IDS)
        self.assertEqual(len(manifest['plugins']), len(IDS))
        for item in manifest['plugins']:
            asset = item['asset']
            raw = (ROOT/'build'/asset['path']).read_bytes()
            self.assertEqual(asset['byteCount'], len(raw))
            self.assertEqual(asset['sha256'], hashlib.sha256(raw).hexdigest())
            self.assertIn('/'+manifest['version']+'/', asset['url'])
            plugin = json.loads(raw)
            # Layout-only plugin follows the official Colemak-DH (enabled, no settings).
            self.assertIs(plugin['enabled'], plugin['id'] == 'rares-qwerty')
            self.assertIn('def ', plugin['source'])
    def test_all_settings_render_without_native_commands(self):
        for plugin in IDS - {'rares-qwerty'}:
            p, calls = load(plugin)
            p['settings'](p['initial']())
            self.assertEqual(calls, [])

if __name__ == '__main__':
    unittest.main()
