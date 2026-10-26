import math


def motor_sizing(power_kw, voltage, power_factor=0.85, efficiency=0.92, poles=4, frequency=60, slip=0.03):
    values = [power_kw, voltage, power_factor, efficiency, frequency, slip]
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in values):
        raise ValueError("Enter finite numeric values.")
    if power_kw <= 0 or voltage <= 0 or not 0 < power_factor <= 1 or not 0 < efficiency <= 1 or poles not in (2, 4, 6, 8) or frequency <= 0 or not 0 <= slip < 1:
        raise ValueError("Check power, voltage, power factor, efficiency, poles, frequency and slip.")
    current = power_kw * 1000 / (math.sqrt(3) * voltage * power_factor * efficiency)
    synchronous = 120 * frequency / poles
    capacity = [(1.5, 15.5), (2.5, 21), (4, 28), (6, 36), (10, 50), (16, 68), (25, 89), (35, 110), (50, 134), (70, 171), (95, 207), (120, 239)]
    section = next((size for size, amps in capacity if amps >= current * 1.25), None)
    breaker = next((amps for amps in (6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 320, 400, 630) if amps >= current * 1.25), None)
    return {"current_a": current, "starting_a": current * 7, "synchronous_rpm": synchronous, "rated_rpm": synchronous * (1 - slip), "cable_mm2": section, "breaker_a": breaker, "thermal_a": current, "fuse_a": next((x for x in (10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630) if x >= current * 1.6), None)}


def voltage_measurement(first, second, line_voltage=380, mode="AC"):
    if first not in ("L1", "L2", "L3", "N", "PE") or second not in ("L1", "L2", "L3", "N", "PE"):
        raise ValueError("invalid_probe")
    if mode == "DC":
        potentials = {"L1": 24, "L2": 0, "L3": 0, "N": 0, "PE": 0}
        return potentials[first] - potentials[second]
    if first == second or {first, second} <= {"N", "PE"}:
        return 0
    return line_voltage if first.startswith("L") and second.startswith("L") else line_voltage / math.sqrt(3)


def bill_of_materials(circuit, current):
    counts = {"dol": 1, "reversal": 2, "star_delta": 3, "traffic": 3, "phase_loss": 1, "vfd": 1}
    items = [("Isolator", 1, "Rated for the supply and load"), ("Short-circuit protection", 1, "Coordinate with the selected equipment"), ("Contactor", counts.get(circuit, 1), f"Select by utilization category and {current:.2f} A load"), ("Overload protection", 1, f"Motor nameplate current; estimate {current:.2f} A"), ("Start / stop controls", 1, "Control voltage and enclosure rating"), ("Terminals, conductors and enclosure", 1, "Select for the installation conditions")]
    if circuit == "reversal":
        items.append(("Mechanical interlock", 1, "Compatible reversing contactors"))
    if circuit == "star_delta":
        items.extend([("Star-delta timer", 1, "Open transition"), ("Mechanical interlock", 1, "Star and delta contactors")])
    if circuit == "phase_loss":
        items.append(("Phase monitoring relay", 1, "Voltage and phase sequence compatible"))
    if circuit == "vfd":
        items.append(("Variable frequency drive", 1, "Match motor, supply, duty and environment"))
    return items
