import ast
import unittest
from html.parser import HTMLParser
from pathlib import Path
from string import Formatter

from electrical import learning, learning_pt
from electrical.circuits import PRESETS
from electrical.i18n import PT, TEMPLATES_PT, error_message, signal_label, translate
from electrical.sizing import bill_of_materials


class LocalizationTests(unittest.TestCase):
    def test_learning_content_has_complete_matching_translations(self):
        for name in ('CHAPTERS', 'BUILD_STEPS'):
            original, translated = getattr(learning, name), getattr(learning_pt, name)
            self.assertEqual(len(original), len(translated))
            for source, target in zip(original, translated):
                self.assertEqual(tuple(translate(x, 'pt-BR') for x in source), target)
                self.assertTrue(all(target))
        self.assertEqual(len(learning.QUESTIONS), len(learning_pt.QUESTIONS))
        for source, target in zip(learning.QUESTIONS, learning_pt.QUESTIONS):
            self.assertEqual(source[2], target[2])
            self.assertEqual(translate(source[0], 'pt-BR'), target[0])
            self.assertEqual([translate(x, 'pt-BR') for x in source[1]], target[1])
            self.assertEqual(translate(source[3], 'pt-BR'), target[3])

    def test_all_presets_and_sequences_are_translated(self):
        for value in PRESETS.values():
            for source in [value['name'], value['detail']] + [step[0] for step in value['steps']]:
                self.assertIn(source, PT)
                self.assertNotEqual(translate(source, 'pt-BR'), source)
                self.assertEqual(translate(source, 'en'), source)

    def test_all_materials_and_dynamic_estimates_are_translated(self):
        for circuit in PRESETS:
            for name, _, reference in bill_of_materials(circuit, 17.25):
                self.assertNotEqual(translate(name, 'pt-BR'), name)
                self.assertNotEqual(translate(reference, 'pt-BR'), reference)

    def test_dynamic_text_and_history_follow_selected_language(self):
        cases = {
            'Step 2 of 9': 'Etapa 2 de 9',
            'Imported 12 projects.': '12 projetos importados.',
            'Question 03': 'Questão 03',
            '2 / 12 correct · progress saved locally': '2 / 12 corretas · progresso salvo localmente',
            '2.0s · FORWARD → ON': '2.0s · DIRETO → LIGADO',
            '3.0s · Alarms acknowledged': '3.0s · Alarmes reconhecidos',
            'Interlock conflict: FORWARD, REVERSE': 'Conflito de intertravamento: DIRETO, REVERSO',
        }
        for source, expected in cases.items():
            self.assertEqual(translate(source, 'pt-BR'), expected)
            self.assertEqual(translate(source, 'en'), source)
        for source, translated in TEMPLATES_PT.items():
            fields = lambda value: {field for _, field, _, _ in Formatter().parse(value) if field}
            self.assertEqual(fields(source), fields(translated))

    def test_interface_shell_labels_and_accessibility_are_translated(self):
        class Labels(HTMLParser):
            def __init__(self):
                super().__init__()
                self.labels = []
            def handle_starttag(self, tag, attrs):
                values = dict(attrs)
                if 'data-i18n' in values:
                    self.labels.append(values['data-i18n'])
        source = Path('index.html').read_text()
        parser = Labels()
        parser.feed(source)
        for label in parser.labels:
            self.assertIn(label, PT)
        self.assertNotIn('Original website', source)
        self.assertNotIn('comandoeletricobrunno.netlify.app', source)
        self.assertIn('value="pt-BR"', source)
        self.assertIn('value="light"', source)
        self.assertIn('[data-theme="light"]', Path('site.css').read_text())

    def test_all_literal_interface_labels_have_catalog_entries(self):
        tree = ast.parse(Path('app.py').read_text())
        positions = {'field': 1, 'text': 1, 'card': 1, 'button': 0, 'element': 1, 'notify': 0}
        invariant = {'JSON ↓', 'SVG ↓'}
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id not in positions:
                continue
            position = positions[node.func.id]
            if len(node.args) <= position:
                continue
            argument = node.args[position]
            if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
                value = argument.value
                if any(char.isalpha() for char in value) and value not in invariant:
                    self.assertIn(value, PT, f'Missing UI translation: {value}')

    def test_errors_and_technical_signal_identifiers(self):
        for message in ('invalid_coils', 'invalid_scan_time', 'invalid_timer_delay', 'missing_signal:START', 'Expecting value: line 1', "could not convert string to float: 'x'"):
            localized = error_message(message, 'pt-BR')
            self.assertNotEqual(localized, message)
            self.assertFalse(localized.startswith(('invalid_', 'Expecting', 'could not')))
        self.assertEqual(signal_label('PHASE_B', 'pt-BR'), 'FASE B')
        self.assertEqual(signal_label('CUSTOM_INPUT', 'en'), 'CUSTOM INPUT')
        self.assertEqual(translate('My custom project', 'pt-BR'), 'My custom project')
        self.assertEqual(translate(12, 'pt-BR'), 12)


if __name__ == '__main__':
    unittest.main()
