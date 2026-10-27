import unittest
from pathlib import Path
from xml.etree import ElementTree

from electrical.circuits import PRESETS, input_signals, preset
from electrical.engine import CircuitEngine
from electrical.guidance import CUSTOM_NOTE, MANUAL_NOTE, STEP_NOTES, output_changes, step_note
from electrical.i18n import translate
from electrical.sizing import motor_sizing, voltage_measurement
from electrical.symbols import SYMBOLS, symbol_svg


class GuidedSimulatorTests(unittest.TestCase):
    def test_every_circuit_step_has_a_short_translated_explanation(self):
        self.assertEqual(set(STEP_NOTES), set(PRESETS))
        for mode, model in PRESETS.items():
            self.assertEqual(len(STEP_NOTES[mode]), len(model['steps']))
            engine = CircuitEngine(model['definition'])
            values = dict(model['inputs'])
            for index, (_, changes) in enumerate(model['steps']):
                values.update(changes)
                result = engine.scan(values, index * 1000)
                english, portuguese = STEP_NOTES[mode][index]
                self.assertTrue(english and portuguese)
                self.assertLessEqual(len(english), 180)
                self.assertLessEqual(len(portuguese), 200)
                self.assertEqual(step_note(mode, index, values, result['coils'], now=index * 1000), english)
                self.assertEqual(translate(english, 'pt-BR'), portuguese)
                self.assertEqual(translate(english, 'en'), english)

    def test_star_delta_titles_match_real_output_states(self):
        model = preset('star_delta')
        engine = CircuitEngine(model['definition'])
        values = model['inputs']
        states = {}
        for index, (title, changes) in enumerate(model['steps']):
            values.update(changes)
            states[title] = engine.scan(values, index * 1000)['coils']
        self.assertTrue(states['Star timer counting']['STAR'])
        self.assertFalse(states['Star timer counting']['STAR_DONE'])
        self.assertTrue(states['Star timer complete']['STAR_DONE'])
        self.assertTrue(states['Star timer complete']['STAR'])
        self.assertFalse(states['Open transition']['STAR'])
        self.assertFalse(states['Open transition']['DELTA'])
        self.assertTrue(states['Delta enabled']['DELTA_READY'])
        self.assertFalse(states['Delta enabled']['DELTA'])
        self.assertTrue(states['Delta operation']['MAIN'])
        self.assertTrue(states['Delta operation']['DELTA'])
        self.assertFalse(states['Delta operation']['STAR'])
        self.assertFalse(states['Stop main contactor']['MAIN'])
        self.assertFalse(any(states['Outputs reset'].values()))
        self.assertTrue(all(value is None for value in engine.timers.values()))

    def test_manual_inputs_and_extra_scans_do_not_get_a_false_scripted_note(self):
        model = preset('dol')
        engine = CircuitEngine(model['definition'])
        values = model['inputs']
        values['START'] = True
        result = engine.scan(values, 0)
        self.assertEqual(step_note('dol', 0, values, result['coils']), MANUAL_NOTE[0])
        self.assertEqual(output_changes(result), (['MOTOR'], []))
        values['STOP'] = True
        result = engine.scan(values, 1000)
        self.assertEqual(output_changes(result), ([], ['MOTOR']))
        self.assertEqual(step_note('dol', 0, values, result['coils'], True), CUSTOM_NOTE[0])
        original = preset('dol')
        self.assertEqual(step_note('dol', 0, original['inputs'], {'MOTOR': False}, now=1000), MANUAL_NOTE[0])
        self.assertEqual(output_changes(None), ([], []))

    def test_110_volts_flows_through_calculations_and_measurements(self):
        self.assertAlmostEqual(motor_sizing(7.5, 110)['current_a'], 2 * motor_sizing(7.5, 220)['current_a'])
        self.assertEqual(voltage_measurement('L1', 'L2', 110), 110)
        self.assertAlmostEqual(voltage_measurement('L1', 'N', 110), 110 / 3 ** .5)
        self.assertIn('(110, "110 V")', Path('app.py').read_text())

    def test_symbol_names_and_svg_labels_are_translated_and_escaped(self):
        seen = set()
        for key, name, name_pt, detail, detail_pt in SYMBOLS:
            self.assertNotIn(key, seen)
            seen.add(key)
            self.assertEqual(translate(name, 'pt-BR'), name_pt)
            self.assertEqual(translate(detail, 'pt-BR'), detail_pt)
            root = ElementTree.fromstring(symbol_svg(key, name_pt))
            self.assertEqual(root.attrib['aria-label'], name_pt)
            self.assertEqual(root.attrib['viewBox'], '0 0 84 56')
        root = ElementTree.fromstring(symbol_svg('coil', 'A "quoted" <label>'))
        self.assertEqual(root.attrib['aria-label'], 'A "quoted" <label>')

    def test_favicon_is_valid_and_included_in_static_site_build(self):
        root = ElementTree.fromstring(Path('favicon.svg').read_text())
        self.assertEqual(root.attrib['viewBox'], '0 0 64 64')
        self.assertIn('href="favicon.svg"', Path('index.html').read_text())
        self.assertIn('"favicon.svg"', Path('scripts/build_site.py').read_text())


if __name__ == '__main__':
    unittest.main()
