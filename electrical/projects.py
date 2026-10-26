import math

from .circuits import LEGACY, PRESETS, preset
from .engine import CircuitEngine


def normalize_project(value):
    if not isinstance(value, dict):
        raise ValueError("Invalid project record.")
    circuit = value.get("circuit", value.get("circuitType", "dol"))
    circuit = LEGACY.get(circuit, circuit)
    if circuit not in PRESETS:
        raise ValueError("Unknown circuit type.")
    name = value.get("name", "Untitled project")
    if not isinstance(name, str) or not name.strip() or len(name) > 120:
        raise ValueError("Project name must contain 1–120 characters.")
    power = float(value.get("power_kw", float(value.get("motorPowerCv", 5)) * 0.73549875))
    voltage = float(value.get("voltage", value.get("motorVoltage", 380)))
    if not math.isfinite(power) or not math.isfinite(voltage) or power <= 0 or voltage <= 0:
        raise ValueError("Power and voltage must be positive finite numbers.")
    definition = value.get("definition", preset(circuit)["definition"])
    CircuitEngine(definition)
    description = value.get("description", "")
    if not isinstance(description, str) or len(description) > 4000:
        raise ValueError("Invalid project description.")
    return {"id": str(value.get("id", ""))[:100], "name": name.strip(), "description": description, "circuit": circuit, "power_kw": power, "voltage": voltage, "definition": definition, "status": str(value.get("status", "draft"))[:40]}


def read_backup(value):
    records = value.get("projects") if isinstance(value, dict) else value
    if not isinstance(records, list) or len(records) > 500:
        raise ValueError("Import a project list or an exported backup with at most 500 projects.")
    return [normalize_project(record) for record in records]
