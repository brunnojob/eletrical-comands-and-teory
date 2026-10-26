import math
import unittest

from electrical import CircuitEngine, structured_text
from electrical.circuits import PRESETS, coil, contact, input_signals, parallel, preset, ton
from electrical.projects import normalize_project, read_backup
from electrical.sizing import motor_sizing, voltage_measurement


class EngineTests(unittest.TestCase):
    def test_seal_in(self):
        engine = CircuitEngine(preset("dol")["definition"])
        values = {"SAFE": True, "STOP": False, "START": True}
        self.assertTrue(engine.scan(values, 0)["coils"]["MOTOR"])
        values["START"] = False
        self.assertTrue(engine.scan(values, 100)["coils"]["MOTOR"])
        values["STOP"] = True
        self.assertFalse(engine.scan(values, 200)["coils"]["MOTOR"])

    def test_snapshot(self):
        coils = [coil("A", contact("INPUT")), coil("B", contact("A"))]
        for order in [coils, list(reversed(coils))]:
            engine = CircuitEngine({"coils": order})
            self.assertEqual(engine.scan({"INPUT": True}, 0)["coils"], {"A": True, "B": False})
            self.assertTrue(engine.scan({"INPUT": True}, 1)["coils"]["B"])

    def test_interlock(self):
        engine = CircuitEngine(preset("reversal")["definition"])
        result = engine.scan({"SAFE": True, "STOP": False, "START_FWD": True, "START_REV": True}, 0)
        self.assertEqual(result["coils"], {"FORWARD": False, "REVERSE": False})
        self.assertEqual(result["interlockTrips"], [["FORWARD", "REVERSE"]])

    def test_timer(self):
        engine = CircuitEngine({"coils": [coil("OUT", ton("DELAY", 100, contact("GO")))]})
        for now, value, expected in [(0, True, False), (99, True, False), (100, True, True), (200, False, False), (300, True, False), (400, True, True)]:
            self.assertEqual(engine.scan({"GO": value}, now)["coils"]["OUT"], expected)

    def test_no_short_circuit(self):
        engine = CircuitEngine({"coils": [coil("OUT", parallel(contact("BYPASS"), ton("DELAY", 100, contact("GO"))))]})
        engine.scan({"BYPASS": True, "GO": True}, 0)
        self.assertTrue(engine.scan({"BYPASS": False, "GO": True}, 100)["coils"]["OUT"])

    def test_transaction(self):
        engine = CircuitEngine({"coils": [coil("A", ton("DELAY", 100, contact("GO"))), coil("B", contact("MISSING"))]})
        with self.assertRaises(ValueError):
            engine.scan({"GO": True}, 0)
        self.assertEqual(engine.timers, {"DELAY": None})
        self.assertEqual(engine.previous_time, -1)
        self.assertEqual(engine.sequence, 0)
        self.assertFalse(engine.scan({"GO": True, "MISSING": False}, 100)["coils"]["A"])

    def test_invalid_time_and_inputs(self):
        for value in [True, -1, .5, math.inf, 9007199254740992]:
            with self.assertRaises(ValueError):
                CircuitEngine(preset("dol")["definition"]).scan(preset("dol")["inputs"], value)
        engine = CircuitEngine(preset("dol")["definition"])
        values = preset("dol")["inputs"]
        engine.scan(values, 0)
        for inputs, now in [(values, 0), ({**values, "MOTOR": False}, 1), ({**values, "START": 1}, 1)]:
            with self.assertRaises(ValueError):
                engine.scan(inputs, now)

    def test_invalid_definitions(self):
        examples = [{"coils": [coil("bad", contact("GO"))]}, {"coils": [coil("OUT", contact(""))]}, {"coils": [coil("OUT", {"type": "and", "children": []})]}, {"coils": [coil("OUT", contact("GO"))], "interlocks": [["OUT", "OUT"]]}, {"coils": [coil("OUT", ton("TIME", -1, contact("GO")))]}]
        for value in examples:
            with self.subTest(value=value), self.assertRaises(ValueError):
                CircuitEngine(value)

    def test_presets(self):
        for key in PRESETS:
            model = preset(key)
            engine = CircuitEngine(model["definition"])
            values = model["inputs"]
            self.assertEqual(set(values), set(input_signals(model["definition"])))
            delta_seen = False
            for index, (_, changes) in enumerate(model["steps"]):
                values.update(changes)
                result = engine.scan(values, index * 1000)
                if key == "star_delta":
                    self.assertFalse(result["coils"]["STAR"] and result["coils"]["DELTA"])
                    delta_seen |= result["coils"]["DELTA"]
            if key == "star_delta":
                self.assertTrue(delta_seen)

    def test_phase_restore(self):
        model = preset("phase_loss")
        engine = CircuitEngine(model["definition"])
        values = model["inputs"]
        values["START"] = True
        self.assertTrue(engine.scan(values, 0)["coils"]["MOTOR"])
        values.update({"START": False, "PHASE_B": False})
        self.assertFalse(engine.scan(values, 1)["coils"]["MOTOR"])
        values["PHASE_B"] = True
        self.assertFalse(engine.scan(values, 2)["coils"]["MOTOR"])


class ExportTests(unittest.TestCase):
    def test_snapshot_export(self):
        text = structured_text(preset("dol")["definition"])
        self.assertIn("P0 := MOTOR;", text)
        self.assertLess(text.index("P0 := MOTOR;"), text.index("N0 :="))
        self.assertTrue(text.endswith("END_FUNCTION_BLOCK\n"))

    def test_collision(self):
        text = structured_text({"coils": [coil("P0", contact("N0"))]})
        self.assertIn("P1 := P0;", text)
        self.assertIn("N1 := N0;", text)

    def test_invalid_export(self):
        for definition, name in [({"coils": [coil("AND", contact("GO"))]}, "Block"), ({"coils": [coil("OUT", contact("BLOCK"))]}, "Block"), ({"coils": []}, "bad-name"), ({"coils": [coil("OUT", ton("DELAY", .5, contact("GO")))]}, "Block")]:
            with self.assertRaises(ValueError):
                structured_text(definition, name)

    def test_nested_timers(self):
        text = structured_text({"coils": [coil("OUT", ton("OUTER", 100, ton("INNER", 50, contact("GO"))))]})
        self.assertLess(text.index("T0(IN := GO"), text.index("T1(IN := T0.Q"))

    def test_presets_export(self):
        for value in PRESETS.values():
            self.assertIn("FUNCTION_BLOCK", structured_text(value["definition"]))


class ToolTests(unittest.TestCase):
    def test_sizing(self):
        value = motor_sizing(7.5, 380)
        self.assertAlmostEqual(value["current_a"], 7500 / (math.sqrt(3) * 380 * .85 * .92))
        self.assertEqual(value["synchronous_rpm"], 1800)
        for args in [(-1, 380), (1, 0), (math.nan, 380), (1, 380, 1.5)]:
            with self.assertRaises(ValueError):
                motor_sizing(*args)

    def test_measurements(self):
        self.assertEqual(voltage_measurement("L1", "L2"), 380)
        self.assertAlmostEqual(voltage_measurement("L1", "N"), 380 / math.sqrt(3))
        self.assertEqual(voltage_measurement("N", "PE"), 0)
        self.assertEqual(voltage_measurement("N", "L1", mode="DC"), -24)

    def test_legacy_import(self):
        project = normalize_project({"name": "Pump", "circuitType": "partida_direta", "motorPowerCv": 5, "motorVoltage": 380})
        self.assertEqual(project["circuit"], "dol")
        self.assertAlmostEqual(project["power_kw"], 3.67749375)
        self.assertEqual(read_backup({"projects": [project]})[0]["name"], "Pump")
        for value in [None, {"name": ""}, {"name": "X", "power_kw": math.inf}, {"name": "X", "definition": {}}]:
            with self.assertRaises((ValueError, TypeError)):
                normalize_project(value)


if __name__ == "__main__":
    unittest.main()
