import copy
import math
import re


def identifier(value):
    return isinstance(value, str) and re.fullmatch(r"[A-Z][A-Z0-9_]{0,31}", value) is not None


class CircuitEngine:
    def __init__(self, definition):
        if not isinstance(definition, dict) or not isinstance(definition.get("coils"), list) or len(definition["coils"]) > 128:
            raise ValueError("invalid_coils")
        self.definition = copy.deepcopy(definition)
        self.coils = {}
        self.timers = {}
        self.previous_time = -1
        self.sequence = 0
        for coil in self.definition["coils"]:
            if not isinstance(coil, dict) or not identifier(coil.get("id")) or coil["id"] in self.coils:
                raise ValueError("invalid_coil_id")
            self.coils[coil["id"]] = False
            self._validate(coil.get("logic"), 0)
        groups = self.definition.get("interlocks", [])
        if not isinstance(groups, list):
            raise ValueError("invalid_interlocks")
        for group in groups:
            if not isinstance(group, list) or len(group) < 2 or any(not isinstance(x, str) for x in group):
                raise ValueError("invalid_interlock")
            if len(set(group)) != len(group) or any(x not in self.coils for x in group):
                raise ValueError("invalid_interlock")

    def _validate(self, node, depth):
        if not isinstance(node, dict) or depth > 32:
            raise ValueError("invalid_logic")
        kind = node.get("type")
        if kind == "contact":
            if not identifier(node.get("signal")) or node.get("mode") not in ("NO", "NC"):
                raise ValueError("invalid_contact")
        elif kind in ("and", "or"):
            children = node.get("children")
            if not isinstance(children, list) or not 1 <= len(children) <= 128:
                raise ValueError("invalid_children")
            for child in children:
                self._validate(child, depth + 1)
        elif kind == "ton":
            delay = node.get("delayMs")
            if not identifier(node.get("id")) or node["id"] in self.timers:
                raise ValueError("invalid_timer_id")
            if isinstance(delay, bool) or not isinstance(delay, (int, float)) or not math.isfinite(delay) or not 0 <= delay <= 3600000:
                raise ValueError("invalid_timer_delay")
            self.timers[node["id"]] = None
            self._validate(node.get("input"), depth + 1)
        else:
            raise ValueError("unknown_logic_type")

    def scan(self, inputs, now):
        if type(now) is not int or not 0 <= now <= 9007199254740991 or now <= self.previous_time:
            raise ValueError("invalid_scan_time")
        if not isinstance(inputs, dict) or any(type(value) is not bool for value in inputs.values()):
            raise ValueError("invalid_inputs")
        if any(key in self.coils for key in inputs):
            raise ValueError("coil_input_override")
        prior = self.coils.copy()
        timers = self.timers.copy()

        def evaluate(node):
            kind = node["type"]
            if kind == "contact":
                signal = node["signal"]
                if signal not in inputs and signal not in prior:
                    raise ValueError("missing_signal:" + signal)
                value = inputs[signal] if signal in inputs else prior[signal]
                return value if node["mode"] == "NO" else not value
            if kind in ("and", "or"):
                values = [evaluate(child) for child in node["children"]]
                return all(values) if kind == "and" else any(values)
            enabled = evaluate(node["input"])
            key = node["id"]
            if not enabled:
                timers[key] = None
                return False
            if timers[key] is None:
                timers[key] = now
            return now - timers[key] >= node["delayMs"]

        next_coils = {coil["id"]: evaluate(coil["logic"]) for coil in self.definition["coils"]}
        trips = [group[:] for group in self.definition.get("interlocks", []) if sum(next_coils[key] for key in group) > 1]
        for group in trips:
            for key in group:
                next_coils[key] = False
        transitions = [{"id": key, "energized": value} for key, value in next_coils.items() if value != prior[key]]
        self.coils = next_coils
        self.timers = timers
        self.previous_time = now
        self.sequence += 1
        return {"sequence": self.sequence, "timestampMs": now, "coils": next_coils.copy(), "transitions": transitions, "interlockTrips": trips}
