import copy


def contact(signal, mode="NO"):
    return {"type": "contact", "signal": signal, "mode": mode}


def series(*nodes):
    return {"type": "and", "children": list(nodes)}


def parallel(*nodes):
    return {"type": "or", "children": list(nodes)}


def ton(key, delay, node):
    return {"type": "ton", "id": key, "delayMs": delay, "input": node}


def coil(key, logic):
    return {"id": key, "logic": logic}


def held(start, output):
    return series(contact("SAFE"), contact("STOP", "NC"), parallel(contact(start), contact(output)))


PRESETS = {
    "dol": {
        "name": "Direct-On-Line", "detail": "Start, seal-in and stop a three-phase motor.",
        "definition": {"coils": [coil("MOTOR", held("START", "MOTOR"))]},
        "inputs": {"SAFE": True, "STOP": False, "START": False},
        "steps": [("Ready", {}), ("Press START", {"START": True}), ("Release START: the auxiliary contact holds", {"START": False}), ("Press STOP", {"STOP": True}), ("Release STOP", {"STOP": False})]},
    "reversal": {
        "name": "Reversal", "detail": "Forward and reverse contactors with electrical interlocks.",
        "definition": {"coils": [coil("FORWARD", series(held("START_FWD", "FORWARD"), contact("REVERSE", "NC"))), coil("REVERSE", series(held("START_REV", "REVERSE"), contact("FORWARD", "NC")))], "interlocks": [["FORWARD", "REVERSE"]]},
        "inputs": {"SAFE": True, "STOP": False, "START_FWD": False, "START_REV": False},
        "steps": [("Ready", {}), ("Forward start", {"START_FWD": True}), ("Forward held", {"START_FWD": False}), ("Stop before reversing", {"STOP": True}), ("Reverse start", {"STOP": False, "START_REV": True}), ("Reverse held", {"START_REV": False}), ("Stop", {"STOP": True})]},
    "star_delta": {
        "name": "Star-Delta", "detail": "Star acceleration, an open transition and delta operation.",
        "definition": {"coils": [coil("MAIN", held("START", "MAIN")), coil("STAR_DONE", ton("STAR_TIME", 3000, contact("MAIN"))), coil("DELTA_READY", ton("DEAD_TIME", 1000, series(contact("MAIN"), contact("STAR_DONE")))), coil("STAR", series(contact("MAIN"), contact("STAR_DONE", "NC"), contact("DELTA", "NC"))), coil("DELTA", series(contact("MAIN"), contact("DELTA_READY"), contact("STAR", "NC")))], "interlocks": [["STAR", "DELTA"]]},
        "inputs": {"SAFE": True, "STOP": False, "START": False},
        "steps": [("Ready", {}), ("Start main contactor", {"START": True}), ("Star acceleration", {"START": False}), ("Star acceleration", {}), ("Star timer counting", {}), ("Star timer complete", {}), ("Open transition", {}), ("Delta enabled", {}), ("Delta operation", {}), ("Stop main contactor", {"STOP": True}), ("Outputs reset", {})]},
    "traffic": {
        "name": "Traffic Light", "detail": "A sequenced signal with mutually exclusive outputs.",
        "definition": {"coils": [coil("RED", contact("RED_REQUEST")), coil("GREEN", contact("GREEN_REQUEST")), coil("YELLOW", contact("YELLOW_REQUEST"))], "interlocks": [["RED", "GREEN", "YELLOW"]]},
        "inputs": {"RED_REQUEST": True, "GREEN_REQUEST": False, "YELLOW_REQUEST": False},
        "steps": [("Red: stop", {}), ("Green: go", {"RED_REQUEST": False, "GREEN_REQUEST": True}), ("Yellow: prepare to stop", {"GREEN_REQUEST": False, "YELLOW_REQUEST": True}), ("Red: stop", {"YELLOW_REQUEST": False, "RED_REQUEST": True})]},
    "phase_loss": {
        "name": "Phase Failure", "detail": "Loss of any phase removes the motor permissive.",
        "definition": {"coils": [coil("MOTOR", series(held("START", "MOTOR"), contact("PHASE_A"), contact("PHASE_B"), contact("PHASE_C")))]},
        "inputs": {"SAFE": True, "STOP": False, "START": False, "PHASE_A": True, "PHASE_B": True, "PHASE_C": True},
        "steps": [("All phases healthy", {}), ("Start motor", {"START": True}), ("Running", {"START": False}), ("Phase B lost: motor trips", {"PHASE_B": False}), ("Phase B restored: restart required", {"PHASE_B": True}), ("Restart", {"START": True})]},
    "vfd": {
        "name": "VFD", "detail": "Enable, run and fault permissives with a frequency reference.",
        "definition": {"coils": [coil("DRIVE_RUN", series(contact("ENABLE"), contact("RUN"), contact("FAULT", "NC")))]},
        "inputs": {"ENABLE": False, "RUN": False, "FAULT": False},
        "steps": [("Drive disabled", {}), ("Enable drive", {"ENABLE": True}), ("Run command", {"RUN": True}), ("Fault removes run", {"FAULT": True}), ("Reset and stop", {"FAULT": False, "RUN": False}), ("Run again", {"RUN": True})]}}

LEGACY = {"partida_direta": "dol", "reversao": "reversal", "estrela_triangulo": "star_delta", "semaforo": "traffic", "falta_fase": "phase_loss", "inversor": "vfd"}


def preset(key):
    return copy.deepcopy(PRESETS[key])


def input_signals(definition):
    coils = {item["id"] for item in definition["coils"]}
    signals = set()

    def visit(node):
        if node["type"] == "contact":
            if node["signal"] not in coils:
                signals.add(node["signal"])
        elif node["type"] == "ton":
            visit(node["input"])
        else:
            for child in node["children"]:
                visit(child)

    for item in definition["coils"]:
        visit(item["logic"])
    return sorted(signals)
