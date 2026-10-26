import re

from .engine import CircuitEngine


RESERVED = set("AND OR NOT XOR TRUE FALSE IF THEN ELSE ELSIF END_IF VAR VAR_INPUT VAR_OUTPUT END_VAR FUNCTION FUNCTION_BLOCK END_FUNCTION END_FUNCTION_BLOCK PROGRAM END_PROGRAM BOOL TON TIME INT REAL CASE OF END_CASE FOR TO DO END_FOR WHILE END_WHILE REPEAT UNTIL END_REPEAT RETURN BOOL_TO_INT".split())


def structured_text(definition, name="BrunnoCircuit"):
    engine = CircuitEngine(definition)
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,31}", name):
        raise ValueError("invalid_block_name")
    used = set(RESERVED)

    def reserve(tag):
        upper = tag.upper()
        if upper in used:
            raise ValueError("reserved_or_duplicate_identifier:" + tag)
        used.add(upper)

    reserve(name)
    for key in engine.coils:
        reserve(key)
    signals = set()

    def collect(node):
        if node["type"] == "contact":
            if node["signal"] not in engine.coils:
                signals.add(node["signal"])
        elif node["type"] == "ton":
            collect(node["input"])
        else:
            for child in node["children"]:
                collect(child)

    for coil in definition["coils"]:
        collect(coil["logic"])
    for signal in sorted(signals):
        reserve(signal)

    def allocate(prefix):
        index = 0
        while prefix + str(index) in used:
            index += 1
        value = prefix + str(index)
        used.add(value)
        return value

    previous = {key: allocate("P") for key in engine.coils}
    following = {key: allocate("N") for key in engine.coils}
    timers = []
    calls = []

    def expression(node):
        kind = node["type"]
        if kind == "contact":
            value = previous.get(node["signal"], node["signal"])
            return value if node["mode"] == "NO" else "(NOT " + value + ")"
        if kind in ("and", "or"):
            return "(" + (" " + kind.upper() + " ").join(expression(child) for child in node["children"]) + ")"
        delay = node["delayMs"]
        if int(delay) != delay:
            raise ValueError("integer_timer_delay_required")
        child = expression(node["input"])
        timer = allocate("T")
        timers.append(timer)
        calls.append(f"{timer}(IN := {child}, PT := T#{int(delay)}ms);")
        return timer + ".Q"

    expressions = {coil["id"]: expression(coil["logic"]) for coil in definition["coils"]}
    lines = ["FUNCTION_BLOCK " + name, "VAR_INPUT"]
    lines += ["  " + key + " : BOOL;" for key in sorted(signals)]
    lines += ["END_VAR", "VAR_OUTPUT"]
    lines += ["  " + key + " : BOOL;" for key in engine.coils]
    lines += ["END_VAR", "VAR"]
    lines += ["  " + key + " : BOOL;" for key in list(previous.values()) + list(following.values())]
    lines += ["  " + key + " : TON;" for key in timers]
    lines += ["END_VAR", ""]
    lines += [previous[key] + " := " + key + ";" for key in engine.coils]
    lines += calls
    lines += [following[key] + " := " + expressions[key] + ";" for key in engine.coils]
    for group in definition.get("interlocks", []):
        total = " + ".join("BOOL_TO_INT(" + following[key] + ")" for key in group)
        lines.append("IF (" + total + ") > 1 THEN")
        lines += ["  " + following[key] + " := FALSE;" for key in group]
        lines.append("END_IF;")
    lines += [key + " := " + following[key] + ";" for key in engine.coils]
    return "\n".join(lines + ["END_FUNCTION_BLOCK", ""])
