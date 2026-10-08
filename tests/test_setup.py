"""Offline hook tests: stubs do NOT validate PyMini/iOS execution."""
import ast
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
IDS = {'period-guard', 'quiet-feedback', 'bilingual-guard', 'explicit-proofread'}

def load(name):
    calls = []
    env = {}
    def builder(name):
        return lambda *args, **kwargs: {'kind': name, 'args': args, 'kwargs': kwargs}
    for key in ['section', 'vstack', 'toggle', 'slider', 'text', 'button', 'bar_button']:
        env[key] = builder(key)
    env['feel'] = builder('feel')
    env['hitbox'] = builder('hitbox')
    env['context'] = lambda: {'selected': ''}
    env['ai_tools'] = lambda action: calls.append(('ai', action))
    env['banner'] = lambda value: calls.append(('banner', value))
    exec(compile((ROOT/'Plugins'/f'{name}.py').read_text(), name, 'exec'), env)
    return env, calls

class BilingualTests(unittest.TestCase):
    def setUp(self):
        self.p, self.calls = load('bilingual-guard')
        self.s = self.p['initial']()
    def test_mixed_sentences_preserved(self):
        sentences = [
            'Ne vedem after the meeting și discutăm deployment-ul.',
            'I can send raportul mâine, please review când ai timp.',
            'Am făcut push pe branch, but tests încă fail.',
            'The actual plan e să mai verificăm feedback-ul.',
            'Sorry, sunt late; ajung în 10 minutes.',
            'Read this: ea are un deal bun, not a bad deal.',
        ]
        for sentence in sentences:
            for token in sentence.split():
                with self.subTest(token=token):
                    self.assertIs(self.p['correct'](token, 'WRONG-LANGUAGE', self.s), False)
        self.assertEqual(self.s, self.p['initial']())
    def test_valid_words_and_ambiguous_ascii(self):
        for token in ['actual', 'care', 'fine', 'data', 'chat', 'sunt', 'și', 'mulțumesc', 'fata', 'fată', 'peste', 'pestei', 'read', 'the', 'RO', 'API']:
            self.assertIs(self.p['correct'](token, 'different', self.s), False)
    def test_special_tokens(self):
        for token in ['https://example.com', 'a@b.ro', '3.14', 'v1.2.3', 's-a', 'mi-am', 'într-un', 'word.word', 'os.path', 'e.g.', 'foo_bar', '12:30']:
            self.assertIs(self.p['correct'](token, 'different', self.s), False)
            self.assertEqual(self.p['suggestions'](token, {'on':True,'suggest':True}), [])
    def test_empty_long_and_nonstring(self):
        for token in ['', 'a'*10000, None, 12]:
            self.assertIs(self.p['correct'](token, 'wrong', self.s), False)
            self.assertEqual(self.p['suggestions'](token, {'on':True,'suggest':True}), [])
    def test_disabled_delegates(self):
        self.s = self.p['on_action']('on', False, self.s)
        self.assertIsNone(self.p['correct']('care', 'wrong', self.s))
    def test_missing_and_corrupted_on_fail_safe(self):
        for state in [{}, {'on':None}, {'on':1}, {'on':'false'}]:
            self.assertIs(self.p['correct']('care', 'wrong', state), False)
    def test_suggestions_opt_in_never_commit(self):
        self.assertEqual(self.p['suggestions']('teh', self.s), [])
        self.s = self.p['on_action']('suggest', True, self.s)
        self.assertEqual(self.p['suggestions']('teh', self.s), ['the'])
        self.assertEqual(self.p['suggestions']('multumesc', self.s), ['mulțumesc'])
        self.assertIs(self.p['correct']('teh', 'the', self.s), False)
    def test_no_case_or_valid_word_suggestions(self):
        state = {'on':True,'suggest':True}
        for token in ['TEH', 'Teh', 'care', 'actual', 'the', 'mulțumesc']:
            self.assertEqual(self.p['suggestions'](token, state), [])
    def test_unknown_action_and_ui_no_effects(self):
        before = dict(self.s)
        self.p['on_action']('unknown', 'text', self.s)
        self.p['settings'](self.s)
        self.assertEqual(before, self.s)
        self.assertEqual(self.calls, [])

class FeedbackTests(unittest.TestCase):
    def setUp(self):
        self.p, self.calls = load('quiet-feedback')
        self.s = self.p['initial']()
    def test_deliberate_all_key_groups(self):
        table = self.p['haptics'](self.s)
        self.assertEqual(set(table), {'letters','keys','space','return','delete','shift'})
        self.assertGreater(table['space']['kwargs']['intensity'], table['letters']['kwargs']['intensity'])
        self.assertLess(table['delete']['kwargs']['intensity'], table['letters']['kwargs']['intensity'])
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
        self.assertEqual(self.p['on_action']('strength', 9, self.s)['strength'], 1.2)
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
            self.assertIs(plugin['enabled'], False)
            self.assertIn('def ', plugin['source'])
    def test_all_settings_render_without_native_commands(self):
        for plugin in IDS:
            p, calls = load(plugin)
            p['settings'](p['initial']())
            self.assertEqual(calls, [])

if __name__ == '__main__':
    unittest.main()
