import copy
import json
import math
from html import escape

from browser import document, html, timer, window
from browser.local_storage import storage

from electrical import CircuitEngine, structured_text
from electrical.circuits import PRESETS, input_signals, preset
from electrical.learning import BUILD_STEPS, CHAPTERS, QUESTIONS
from electrical.projects import normalize_project, read_backup
from electrical.sizing import bill_of_materials, motor_sizing, voltage_measurement


KEY = "brunno_electrical_python_v1"
state = {"page": "Simulator", "mode": "dol", "step": 0, "clock": -1000, "running": None, "zoom": 1, "events": [], "alarms": [], "project_id": "", "question": 0, "answered": None}
workspace = {"projects": [], "answers": {}, "checklist": {}, "voltage": 380, "frequency": 60}
engine = None
inputs = {}
definition = {}
active_preset = None
storage_ok = True


def notify(message, error=False):
    document["notification"].text = message
    document["notification"].class_name = "error" if error else ""


def save():
    global storage_ok
    try:
        storage[KEY] = json.dumps(workspace)
        storage_ok = True
        return True
    except Exception:
        storage_ok = False
        notify("Browser storage is unavailable or full. Export a backup before closing this page.", True)
        return False


def load():
    try:
        if KEY in storage:
            value = json.loads(storage[KEY])
            workspace["projects"] = read_backup(value)
            workspace["answers"] = value.get("answers", {})
            workspace["checklist"] = value.get("checklist", {})
            workspace["voltage"] = float(value.get("voltage", 380))
            workspace["frequency"] = float(value.get("frequency", 60))
        elif "brunno_projects_v1" in storage:
            workspace["projects"] = read_backup(json.loads(storage["brunno_projects_v1"]))
            save()
    except Exception:
        notify("Saved data could not be read. The original storage was left untouched; import a valid backup to recover it.", True)


def element(tag, text=None, cls=None, **attrs):
    item = getattr(html, tag.upper())(**attrs)
    if text is not None:
        item.text = str(text)
    if cls:
        item.class_name = cls
    return item


def button(text, callback, cls="", target=None):
    item = element("button", text, cls, type="button")
    item.bind("click", callback)
    if target is not None:
        target <= item
    return item


def field(parent, label, value="", kind="text", options=None, key=None):
    box = element("div", cls="field")
    uid = key or "field-" + str(len(document.select("input,select,textarea")))
    lab = element("label", label)
    lab.attrs["for"] = uid
    box <= lab
    if options is not None:
        item = element("select", id=uid)
        for option in options:
            option_value, option_label = option if isinstance(option, tuple) else (option, option)
            opt = element("option", option_label, value=str(option_value))
            item <= opt
        item.value = str(value)
    else:
        item = element("textarea" if kind == "textarea" else "input", id=uid)
        if kind != "textarea":
            item.type = kind
        if kind == "number":
            item.attrs["step"] = "any"
        item.value = str(value)
    box <= item
    parent <= box
    return item


def card(parent, title=None, cls=""):
    item = element("section", cls="card " + cls)
    if title:
        item <= element("h2", title)
    parent <= item
    return item


def text(parent, value, cls=None, tag="p"):
    item = element(tag, value, cls)
    parent <= item
    return item


def toolbar(parent):
    item = element("div", cls="toolbar")
    parent <= item
    return item


def download(filename, content, media="application/json"):
    blob = window.Blob.new([content], {"type": media})
    url = window.URL.createObjectURL(blob)
    anchor = html.A(href=url, download=filename)
    document <= anchor
    anchor.click()
    anchor.remove()
    timer.set_timeout(lambda: window.URL.revokeObjectURL(url), 1000)


def table(parent, headers, rows):
    tab = html.TABLE()
    heading = html.TR()
    for value in headers:
        heading <= html.TH(str(value))
    tab <= html.THEAD(heading)
    body = html.TBODY()
    for row in rows:
        line = html.TR()
        for value in row:
            line <= html.TD(str(value))
        body <= line
    tab <= body
    parent <= tab


def stop():
    if state["running"] is not None:
        timer.clear_interval(state["running"])
        state["running"] = None


def select_page(name):
    stop()
    state["page"] = name
    render()


def reset_simulation(mode=None, custom=None):
    global engine, inputs, definition, active_preset
    stop()
    if mode is not None:
        state["mode"] = mode
    active_preset = preset(state["mode"])
    definition = copy.deepcopy(custom if custom is not None else active_preset["definition"])
    engine = CircuitEngine(definition)
    inputs = {key: active_preset["inputs"].get(key, False) for key in input_signals(definition)}
    state.update({"step": 0, "clock": -1000, "events": [], "alarms": [], "custom": custom is not None})
    scan()


def scan():
    state["clock"] += 1000
    try:
        result = engine.scan(inputs, state["clock"])
        for change in result["transitions"]:
            state["events"].insert(0, f'{state["clock"] / 1000:.1f}s · {change["id"]} → {"ON" if change["energized"] else "OFF"}')
        for group in result["interlockTrips"]:
            alarm = "Interlock conflict: " + ", ".join(group)
            if alarm not in state["alarms"]:
                state["alarms"].append(alarm)
            state["events"].insert(0, f'{state["clock"] / 1000:.1f}s · {alarm}')
        if any(key.startswith("PHASE_") and not value for key, value in inputs.items()):
            if "Phase failure" not in state["alarms"]:
                state["alarms"].append("Phase failure")
                state["events"].insert(0, f'{state["clock"] / 1000:.1f}s · Phase failure')
        state["events"] = state["events"][:100]
        return result
    except ValueError as error:
        stop()
        notify(str(error), True)
        return None


def next_step(event=None):
    if state["custom"]:
        scan()
    elif state["step"] < len(active_preset["steps"]) - 1:
        state["step"] += 1
        inputs.update(active_preset["steps"][state["step"]][1])
        scan()
    else:
        stop()
    if state["page"] == "Simulator":
        render_simulator_content()


def previous_step(event=None):
    desired = max(0, state["step"] - 1)
    reset_simulation(custom=definition if state["custom"] else None)
    for _ in range(desired):
        state["step"] += 1
        inputs.update(active_preset["steps"][state["step"]][1])
        scan()
    render_simulator_content()


def auto(event=None):
    if state["running"] is not None:
        stop()
    else:
        state["running"] = timer.set_interval(next_step, 1200)
    render_simulator_content()


def change_input(event, key):
    inputs[key] = bool(event.target.checked)
    scan()
    render_simulator_content()


def logic_text(node):
    kind = node["type"]
    if kind == "contact":
        return ("NOT " if node["mode"] == "NC" else "") + node["signal"]
    if kind == "ton":
        return f'TON {node["id"]} ({node["delayMs"]} ms): ' + logic_text(node["input"])
    return "(" + (" AND " if kind == "and" else " OR ").join(logic_text(child) for child in node["children"]) + ")"


def diagram_svg():
    width = 1000
    height = 160 + len(definition["coils"]) * 85
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Electrical control schematic" viewBox="0 0 {width} {height}">', '<g font-family="monospace" font-size="13" fill="#91a2b9">']
    parts.append('<text x="30" y="30">POWER OVERVIEW · SIMPLIFIED</text>')
    labels = ["3~ SUPPLY", "ISOLATOR", "PROTECTION", "CONTACTOR / DRIVE", "MOTOR / LOAD"]
    energized = any(value for key, value in engine.coils.items() if key not in ("STAR_DONE", "DELTA_READY"))
    for index, label in enumerate(labels):
        x = 30 + index * 195
        color = "#a5ed68" if energized else "#53677f"
        if index:
            parts.append(f'<path d="M{x-40} 72H{x}" fill="none" stroke="{color}" stroke-width="2"/>')
        parts.append(f'<rect x="{x}" y="48" width="155" height="48" rx="5" fill="#142130" stroke="{color}"/><text x="{x+77.5}" y="77" text-anchor="middle" font-size="10">{label}</text>')
    parts.append('<text x="30" y="130">CONTROL LOGIC · PREVIOUS-SCAN FEEDBACK</text>')
    for index, output in enumerate(definition["coils"]):
        y = 165 + index * 85
        color = "#a5ed68" if engine.coils[output["id"]] else "#53677f"
        label = logic_text(output["logic"])
        lines = [label[i:i+90] for i in range(0, len(label), 90)]
        parts.append(f'<path d="M30 {y}H70M800 {y}H855M905 {y}H960" stroke="{color}" stroke-width="2" fill="none"/><rect x="70" y="{y-20}" width="730" height="55" rx="5" fill="#111d2a" stroke="{color}"/>')
        for line, content in enumerate(lines[:3]):
            parts.append(f'<text x="85" y="{y-2+line*15}" font-size="11">{escape(content)}</text>')
        parts.append(f'<circle cx="880" cy="{y}" r="25" fill="#142130" stroke="{color}" stroke-width="2"/><text x="880" y="{y+45}" text-anchor="middle" fill="{color}" font-size="11">{escape(output["id"])}</text>')
    parts.append('</g></svg>')
    return "".join(parts)


def render_simulator(parent):
    top = card(parent)
    row = element("div", cls="grid equal")
    top <= row
    mode = field(row, "Circuit", state["mode"], options=[(key, value["name"]) for key, value in PRESETS.items()], key="circuit")
    mode.bind("change", lambda event: switch_mode(event.target.value))
    supply = field(row, "Line voltage", workspace["voltage"], options=[(220, "220 V"), (380, "380 V"), (440, "440 V"), (660, "660 V")], key="supply")
    supply.bind("change", lambda event: update_supply(event.target.value))
    text(top, active_preset["detail"], "subtle")
    content = element("div", id="simulation-content")
    parent <= content
    render_simulator_content()


def switch_mode(mode):
    reset_simulation(mode)
    render()


def update_supply(value):
    workspace["voltage"] = float(value)
    save()


def render_simulator_content():
    parent = document["simulation-content"]
    parent.clear()
    metrics = element("div", cls="metrics")
    parent <= metrics
    for title, value, unit in [("Scan time", f'{state["clock"]/1000:.1f}', "s"), ("Active outputs", sum(engine.coils.values()), "/ " + str(len(engine.coils))), ("Sequence", engine.sequence, "scans")]:
        metric = element("div", cls="metric")
        metric <= element("label", title)
        val = element("div", cls="value")
        val <= str(value)
        val <= element("span", unit, "unit")
        metric <= val
        metrics <= metric
    grid = element("div", cls="grid two")
    parent <= grid
    drawing = card(grid)
    head = element("div", cls="card-head")
    head <= element("h2", "Single-line & control diagram")
    actions = toolbar(head)
    button("−", lambda event: zoom(-0.25), "small", actions)
    button("Fit", lambda event: zoom(0), "small", actions)
    button("+", lambda event: zoom(0.25), "small", actions)
    button("SVG ↓", lambda event: download("circuit.svg", diagram_svg(), "image/svg+xml"), "small", actions)
    drawing <= head
    diagram = element("div", cls="diagram", id="diagram")
    diagram.html = diagram_svg()
    diagram.select("svg")[0].style.width = str(state["zoom"] * 100) + "%"
    drawing <= diagram
    step = element("div", cls="step")
    step <= element("small", "Manual scan" if state["custom"] else f'Step {state["step"]+1} of {len(active_preset["steps"])}')
    step <= element("span", "Custom circuit: toggle inputs and advance scans." if state["custom"] else active_preset["steps"][state["step"]][0])
    drawing <= step
    controls = toolbar(drawing)
    button("← Previous", previous_step, target=controls).disabled = state["custom"] or state["step"] == 0
    button("Pause" if state["running"] is not None else "Auto play", auto, "primary", controls)
    button("Next scan →" if state["custom"] else "Next step →", next_step, target=controls)
    button("Reset", lambda event: reset_and_render(), target=controls)
    text(drawing, "Every scan advances simulated time by 1 second. Coil feedback is visible on the next scan. The diagram is conceptual.", "subtle")
    side = card(grid, "Input signals")
    for key, value in inputs.items():
        box = element("div", cls="check")
        check = html.INPUT(type="checkbox", id="input-" + key)
        check.checked = value
        check.bind("change", lambda event, key=key: change_input(event, key))
        label = html.LABEL(key.replace("_", " "), **{"for": "input-" + key})
        box <= check
        box <= label
        side <= box
    text(side, "Outputs", tag="h3")
    for key, value in engine.coils.items():
        row = element("div", cls="signal")
        row <= element("code", key)
        status = element("span", cls="on" if value else "off")
        status <= element("span", cls="led")
        status <= "ON" if value else "OFF"
        row <= status
        side <= row
    if state["mode"] == "vfd":
        freq = field(side, "Frequency reference (Hz)", workspace["frequency"], "number", key="vfd-frequency")
        result = text(side, f'Modeled 4-pole synchronous speed: {120 * workspace["frequency"] / 4:.0f} rpm' if engine.coils.get("DRIVE_RUN") else "Drive stopped", "subtle")
        def set_frequency(event):
            try:
                value = float(freq.value)
                if not math.isfinite(value) or not 0 <= value <= 120:
                    raise ValueError("Use a frequency between 0 and 120 Hz.")
                workspace["frequency"] = value
                save()
                result.text = f'Modeled 4-pole synchronous speed: {value * 30:.0f} rpm' if engine.coils.get("DRIVE_RUN") else "Drive stopped"
            except ValueError as error:
                notify(str(error), True)
        freq.bind("change", set_frequency)
    logs = card(parent, "Events & alarms")
    if state["alarms"]:
        text(logs, " · ".join(state["alarms"]), "alert")
        button("Acknowledge alarms", acknowledge, "small", logs)
    history = element("div", cls="event-log")
    for event in state["events"]:
        history <= element("div", event)
    if not state["events"]:
        text(history, "No transitions yet. Start the sequence or toggle an input.", "empty")
    logs <= history
    with_code = element("details")
    with_code <= element("summary", "Circuit editor & PLC export")
    text(with_code, "Edit NO / NC contacts, AND / OR branches, TON timers, coils and interlock groups. Loading an invalid definition preserves the current circuit.")
    editor = field(with_code, "Circuit JSON", json.dumps(definition, indent=2), "textarea", key="circuit-json")
    editor.rows = 16
    controls = toolbar(with_code)
    def load_definition(event):
        try:
            value = json.loads(editor.value)
            CircuitEngine(value)
            reset_simulation(custom=value)
            render()
            notify("Custom circuit loaded.")
        except (ValueError, TypeError, KeyError) as error:
            notify(str(error), True)
    button("Load circuit", load_definition, target=controls)
    button("JSON ↓", lambda event: download("circuit.json", json.dumps(definition, indent=2)), target=controls)
    def export_st(event):
        try:
            download("circuit.st", structured_text(definition), "text/plain")
        except ValueError as error:
            notify(str(error), True)
    button("Structured Text ↓", export_st, target=controls)
    parent <= with_code


def reset_and_render():
    reset_simulation(custom=definition if state["custom"] else None)
    render_simulator_content()


def acknowledge(event):
    state["alarms"] = []
    state["events"].insert(0, f'{state["clock"]/1000:.1f}s · Alarms acknowledged')
    render_simulator_content()


def zoom(delta):
    state["zoom"] = 1 if delta == 0 else max(0.75, min(3.5, state["zoom"] + delta))
    render_simulator_content()


def render_theory(parent):
    search = field(parent, "Search topics", "", key="theory-search")
    search.class_name = "search"
    contents = element("div")
    parent <= contents
    def show(event=None):
        contents.clear()
        query = search.value.lower()
        for index, (title, body) in enumerate(CHAPTERS):
            if query not in (title + body).lower():
                continue
            details = element("details")
            details <= element("summary", f'{index+1:02d} · {title}')
            text(details, body)
            contents <= details
    search.bind("input", show)
    show()


def render_sizing(parent):
    grid = element("div", cls="grid equal")
    parent <= grid
    form = card(grid, "Motor data")
    fields = {}
    for key, label, value in [("power", "Mechanical output power (kW)", 7.5), ("voltage", "Line voltage (V)", workspace["voltage"]), ("pf", "Power factor (0–1)", .85), ("efficiency", "Efficiency (0–1)", .92)]:
        fields[key] = field(form, label, value, "number", key="size-" + key)
    fields["poles"] = field(form, "Poles", 4, options=[2, 4, 6, 8], key="size-poles")
    fields["hz"] = field(form, "Frequency (Hz)", 60, options=[50, 60], key="size-hz")
    fields["slip"] = field(form, "Estimated slip (0–1)", .03, "number", key="size-slip")
    output = card(grid, "Calculation results")
    def calculate(event=None):
        try:
            result = motor_sizing(float(fields["power"].value), float(fields["voltage"].value), float(fields["pf"].value), float(fields["efficiency"].value), int(fields["poles"].value), float(fields["hz"].value), float(fields["slip"].value))
            output.clear()
            text(output, "Calculation results", tag="h2")
            table(output, ["Parameter", "Estimate"], [("Rated current", f'{result["current_a"]:.2f} A'), ("DOL starting current (7×)", f'{result["starting_a"]:.2f} A'), ("Synchronous speed", f'{result["synchronous_rpm"]:.0f} rpm'), ("Speed with estimated slip", f'{result["rated_rpm"]:.0f} rpm'), ("Illustrative copper section", str(result["cable_mm2"]) + " mm²" if result["cable_mm2"] else "Outside table"), ("Illustrative breaker (1.25×)", str(result["breaker_a"]) + " A" if result["breaker_a"] else "Outside table"), ("Overload current reference", f'{result["thermal_a"]:.2f} A'), ("Illustrative fuse (1.6×)", str(result["fuse_a"]) + " A" if result["fuse_a"] else "Outside table")])
            text(output, "I = P / (√3 × V × power factor × efficiency). Starting current uses an assumed multiplier. Cable and protective-device values are study examples, not installation selections; check installation method, derating, voltage drop, fault level, starting duty and manufacturer coordination.", "note")
            button("Results JSON ↓", lambda event: download("motor-sizing.json", json.dumps(result, indent=2)), target=output)
        except ValueError as error:
            notify(str(error), True)
    button("Calculate", calculate, "primary", form)
    calculate()
    conversions = card(parent, "Power conversion")
    row = element("div", cls="grid three")
    conversions <= row
    value = field(row, "Value", 1, "number", key="convert-value")
    unit = field(row, "From", "kW", options=["kW", "CV", "HP"], key="convert-unit")
    result = text(row, "", "value")
    def convert(event=None):
        try:
            number = float(value.value)
            if not math.isfinite(number) or number < 0:
                raise ValueError("Enter a nonnegative finite power.")
            kw = number * {"kW": 1, "CV": .73549875, "HP": .745699872}[unit.value]
            result.text = f'{kw:.3f} kW · {kw/.73549875:.3f} CV · {kw/.745699872:.3f} HP'
        except ValueError as error:
            notify(str(error), True)
    value.bind("input", convert)
    unit.bind("change", convert)
    convert()


def render_multimeter(parent):
    box = card(parent, "Virtual multimeter")
    text(box, "Simulated readings only. AC uses a balanced three-phase supply with an ideal N–PE bond; DC uses L1 = +24 V and all other points = 0 V.")
    row = element("div", cls="grid three")
    box <= row
    function = field(row, "Measurement", "AC voltage", options=["AC voltage", "DC voltage", "AC current", "Continuity"], key="meter-function")
    red = field(row, "Red probe", "L1", options=["L1", "L2", "L3", "N", "PE"], key="meter-red")
    black = field(row, "Black probe", "L2", options=["L1", "L2", "L3", "N", "PE"], key="meter-black")
    meter = element("div", cls="meter")
    box <= meter
    description = text(box, "", "note")
    def measure(event=None):
        mode = function.value
        if mode in ("AC voltage", "DC voltage"):
            value = voltage_measurement(red.value, black.value, workspace["voltage"], "DC" if mode == "DC voltage" else "AC")
            unit = "V DC" if mode == "DC voltage" else "V AC"
            description.text = "The model assumes an ideal balanced supply. Actual readings depend on the real circuit and equipment."
        elif mode == "AC current":
            current = motor_sizing(7.5, workspace["voltage"])["current_a"]
            value = current if red.value.startswith("L") and any(engine.coils.values()) else 0
            unit = "A AC"
            description.text = "Modeled clamp reading on the selected red-probe conductor for a 7.5 kW load. The black probe is unused in clamp mode. No live measurement is performed."
        else:
            value = "0.0" if red.value == black.value or {red.value, black.value} <= {"N", "PE"} else "OL"
            unit = "Ω / continuity"
            description.text = "A separate de-energized topology model is used here. It assumes an N–PE bond and no path between different phase points. This does not describe or verify any physical installation."
        meter.clear()
        meter <= element("small", unit)
        meter <= (f'{value:.1f}' if isinstance(value, (int, float)) else value)
    for control in (function, red, black):
        control.bind("change", measure)
    measure()
    plate = card(parent, "Reading a motor nameplate")
    table(plate, ["Marking", "Meaning"], [("kW / HP / CV", "Mechanical shaft output power"), ("V · Δ / Y", "Rated voltage for each winding connection"), ("A", "Rated current for the specified connection and duty"), ("Hz / rpm", "Rated frequency and shaft speed"), ("cos φ / η", "Power factor and efficiency"), ("IP / duty / insulation", "Environmental protection, operating duty and insulation classification")])


def new_id():
    return str(int(window.Date.now())) + "-" + str(int(window.Math.random() * 1000000))


def export_backup(event=None):
    download("electrical-workspace.json", json.dumps({"version": 1, **workspace}, indent=2))


def import_backup(event):
    if not event.target.files.length:
        return
    file = event.target.files[0]
    if file.size > 2000000:
        notify("Import files must be smaller than 2 MB.", True)
        return
    reader = window.FileReader.new()
    def loaded(event):
        try:
            data = json.loads(reader.result)
            projects = read_backup(data)
            merged = copy.deepcopy(workspace["projects"])
            for project in projects:
                project["id"] = new_id()
                merged.append(project)
            if len(merged) > 500:
                raise ValueError("The workspace can hold at most 500 projects.")
            workspace["projects"] = merged
            if isinstance(data, dict):
                if isinstance(data.get("answers"), dict):
                    workspace["answers"].update(data["answers"])
                if isinstance(data.get("checklist"), dict):
                    workspace["checklist"].update(data["checklist"])
            saved = save()
            render()
            if saved:
                notify(f"Imported {len(projects)} projects.")
        except (ValueError, TypeError, KeyError) as error:
            notify(str(error), True)
    reader.bind("load", loaded)
    reader.bind("error", lambda event: notify("The selected file could not be read.", True))
    reader.readAsText(file)


def import_control(parent):
    label = element("label", "Import JSON", "file-label")
    control = html.INPUT(type="file", accept="application/json,.json")
    control.bind("change", import_backup)
    label <= control
    parent <= label


def project_form(parent, existing=None):
    item = card(parent, "Edit project" if existing else "New project")
    form = element("div", cls="grid equal")
    item <= form
    name = field(form, "Project name", existing["name"] if existing else "", key="project-name")
    circuit = field(form, "Circuit", existing["circuit"] if existing else state["mode"], options=[(key, value["name"]) for key, value in PRESETS.items()], key="project-circuit")
    power = field(form, "Motor power (kW)", existing["power_kw"] if existing else 3.7, "number", key="project-power")
    voltage = field(form, "Voltage (V)", existing["voltage"] if existing else workspace["voltage"], "number", key="project-voltage")
    description = field(item, "Description", existing["description"] if existing else "", "textarea", key="project-description")
    status = field(item, "Status", existing.get("status", "draft") if existing else "draft", options=["draft", "review", "ready"], key="project-status")
    def submit(event):
        try:
            value = {"id": existing["id"] if existing else new_id(), "name": name.value, "circuit": circuit.value, "power_kw": float(power.value), "voltage": float(voltage.value), "description": description.value, "status": status.value}
            if existing and existing["circuit"] == circuit.value:
                value["definition"] = existing["definition"]
            elif not existing and state["custom"] and circuit.value == state["mode"]:
                value["definition"] = definition
            project = normalize_project(value)
            if existing:
                workspace["projects"] = [project if x["id"] == existing["id"] else x for x in workspace["projects"]]
            else:
                if len(workspace["projects"]) >= 500:
                    raise ValueError("Export and remove projects before adding more than 500.")
                workspace["projects"].append(project)
            state["editing"] = None
            saved = save()
            render()
            if saved:
                notify("Project saved in this browser.")
        except (ValueError, TypeError) as error:
            notify(str(error), True)
    controls = toolbar(item)
    button("Save project", submit, "primary", controls)
    if existing:
        button("Cancel", lambda event: cancel_edit(), target=controls)


def cancel_edit():
    state["editing"] = None
    render()


def open_project(project):
    state["project_id"] = project["id"]
    workspace["voltage"] = project["voltage"]
    reset_simulation(project["circuit"], project["definition"])
    state["page"] = "Simulator"
    render()


def edit_project(project):
    state["editing"] = project["id"]
    render()


def duplicate_project(project):
    value = copy.deepcopy(project)
    value["id"] = new_id()
    value["name"] = value["name"][:110] + " (copy)"
    if len(workspace["projects"]) >= 500:
        notify("The workspace can hold at most 500 projects.", True)
        return
    workspace["projects"].append(value)
    save()
    render()


def delete_project(project, container):
    container.clear()
    text(container, 'Remove "' + project["name"] + '" from this browser? Export a backup first if needed.')
    controls = toolbar(container)
    def remove(event):
        workspace["projects"] = [x for x in workspace["projects"] if x["id"] != project["id"]]
        save()
        render()
    button("Remove project", remove, "danger", controls)
    button("Cancel", lambda event: render(), target=controls)


def render_projects(parent):
    controls = toolbar(parent)
    button("Export backup ↓", export_backup, target=controls)
    import_control(controls)
    editing = next((x for x in workspace["projects"] if x["id"] == state.get("editing")), None)
    project_form(parent, editing)
    text(parent, "Saved projects", tag="h2")
    projects = element("div", cls="grid three")
    parent <= projects
    for project in workspace["projects"]:
        item = card(projects, cls="project-card")
        text(item, PRESETS[project["circuit"]]["name"] + " · " + project["status"], "tag", "span")
        text(item, project["name"], tag="h3")
        text(item, project["description"] or "No description.", "subtle")
        text(item, f'{project["power_kw"]:.2f} kW · {project["voltage"]:g} V', "subtle")
        controls = toolbar(item)
        button("Open", lambda event, p=project: open_project(p), "primary small", controls)
        button("Edit", lambda event, p=project: edit_project(p), "small", controls)
        button("Copy", lambda event, p=project: duplicate_project(p), "small", controls)
        button("JSON ↓", lambda event, p=project: download("project.json", json.dumps({"projects": [p]}, indent=2)), "small", controls)
        button("Remove", lambda event, p=project, c=item: delete_project(p, c), "small danger", controls)
    if not workspace["projects"]:
        text(projects, "No saved projects yet. Create one above or use a template below.", "empty wide")
    text(parent, "Ready-to-use templates", tag="h2")
    templates = element("div", cls="grid three")
    parent <= templates
    for key, data in PRESETS.items():
        item = card(templates, data["name"])
        text(item, data["detail"], "subtle")
        def use(event, key=key):
            value = normalize_project({"name": PRESETS[key]["name"] + " project", "circuit": key, "power_kw": 3.7, "voltage": 380, "id": new_id()})
            if len(workspace["projects"]) >= 500:
                notify("The workspace can hold at most 500 projects.", True)
                return
            workspace["projects"].append(value)
            save()
            render()
        button("Use template", use, "small", item)
    text(parent, "Storage is specific to this browser and site address. Netlify data does not automatically move to GitHub Pages. JSON imports also accept the original site's project records.", "note")


def render_build(parent):
    box = card(parent, "Project plan & materials")
    options = [("current", "Current simulator circuit")] + [(x["id"], x["name"]) for x in workspace["projects"]]
    selector = field(box, "Project", state.get("build_project", "current"), options=options, key="build-project")
    selector.bind("change", lambda event: choose_build(event.target.value))
    project = next((x for x in workspace["projects"] if x["id"] == selector.value), None)
    mode = project["circuit"] if project else state["mode"]
    power = project["power_kw"] if project else 7.5
    voltage = project["voltage"] if project else workspace["voltage"]
    current = motor_sizing(power, voltage)["current_a"]
    text(box, f'{PRESETS[mode]["name"]} · {power:.2f} kW · {voltage:g} V · estimated rated current {current:.2f} A')
    table(box, ["Item", "Quantity", "Selection reference"], bill_of_materials(mode, current))
    text(box, "Planning aid for study. Final wiring, ratings and protection settings require a reviewed design and manufacturer documentation.", "note")
    controls = toolbar(box)
    button("Materials CSV ↓", lambda event: download("materials.csv", "Item,Quantity,Selection reference\n" + "\n".join(','.join('"' + str(cell).replace('"', '""') + '"' for cell in row) for row in bill_of_materials(mode, current)), "text/csv"), target=controls)
    button("Print / PDF", lambda event: window.print(), target=controls)
    checklist = card(parent, "Build & review checklist")
    prefix = selector.value
    completed = workspace["checklist"].get(prefix, [])
    for index, (title, body) in enumerate(BUILD_STEPS):
        row = element("div", cls="check")
        check = html.INPUT(type="checkbox", id="build-" + str(index))
        check.checked = index in completed
        def checked(event, index=index):
            values = workspace["checklist"].get(prefix, [])
            values = [value for value in values if value != index]
            if event.target.checked:
                values.append(index)
            workspace["checklist"][prefix] = values
            save()
        check.bind("change", checked)
        label = html.LABEL(**{"for": "build-" + str(index)})
        label <= element("strong", f'{index+1}. {title}')
        label <= element("p", body, "subtle")
        row <= check
        row <= label
        checklist <= row


def choose_build(value):
    state["build_project"] = value
    render()


def render_training(parent):
    index = state["question"]
    question, options, correct, explanation = QUESTIONS[index]
    answered = workspace["answers"]
    total = sum(value is True for value in answered.values())
    box = card(parent)
    text(box, f'{total} / {len(QUESTIONS)} correct · progress saved locally', "subtle")
    progress = element("div", cls="progress")
    bar = element("div")
    bar.style.width = str(total / len(QUESTIONS) * 100) + "%"
    progress <= bar
    box <= progress
    text(box, f'Question {index+1:02d}', "eyebrow")
    text(box, question, tag="h2")
    for position, option in enumerate(options):
        cls = "answer"
        if state["answered"] is not None:
            if position == correct:
                cls += " correct"
            elif position == state["answered"]:
                cls += " wrong"
        def answer(event, position=position):
            state["answered"] = position
            workspace["answers"][str(index)] = position == correct
            save()
            render()
        button(option, answer, cls, box).disabled = state["answered"] is not None
    if state["answered"] is not None:
        text(box, ("Correct. " if state["answered"] == correct else "Try again. ") + explanation, "note")
    controls = toolbar(box)
    button("← Previous", lambda event: question_at(index - 1), target=controls).disabled = index == 0
    button("Retry", lambda event: question_at(index), target=controls)
    button("Next →", lambda event: question_at(index + 1), "primary", controls).disabled = index == len(QUESTIONS) - 1
    text(parent, "Practice in the simulator", tag="h2")
    grid = element("div", cls="grid three")
    parent <= grid
    for key, challenge in [("dol", "Start the motor, release START, then test STOP."), ("reversal", "Request both directions and inspect the conflict event."), ("star_delta", "Advance scans and observe star release before delta starts."), ("phase_loss", "Remove PHASE B while running. Restore it and test restart."), ("traffic", "Follow red, green and yellow without overlapping outputs."), ("vfd", "Compare enable, run and fault signals.")]:
        item = card(grid, PRESETS[key]["name"])
        text(item, challenge)
        button("Open simulator", lambda event, key=key: training_simulator(key), "small", item)


def question_at(index):
    state["question"] = index
    state["answered"] = None
    render()


def training_simulator(key):
    reset_simulation(key)
    select_page("Simulator")


PAGES = {"Simulator": ("ϟ", "Explore electrical control sequences and test the logic, one scan at a time.", render_simulator), "Theory": ("▤", "The principles behind motors, protection and electrical control.", render_theory), "Motor Sizing": ("◈", "Estimate motor current, speed and component references.", render_sizing), "Multimeter": ("⌁", "Explore voltage, current and continuity in a virtual circuit.", render_multimeter), "Projects": ("▦", "Create, organize and back up projects in your browser.", render_projects), "How to Build": ("⚒", "Plan materials and track your design review.", render_build), "Training": ("◎", "Test your knowledge and practice with circuit challenges.", render_training)}


def render():
    navigation = document["navigation"]
    navigation.clear()
    for name, (icon, _, _) in PAGES.items():
        item = button("", lambda event, name=name: select_page(name), "active" if state["page"] == name else "", navigation)
        item <= element("span", icon)
        item <= name
        if state["page"] == name:
            item.attrs["aria-current"] = "page"
    parent = document["app"]
    parent.clear()
    heading = element("div", cls="page-head")
    title = element("div")
    title <= element("div", "ELECTRICAL CONTROLS LAB", "eyebrow")
    title <= element("h1", state["page"])
    title <= element("p", PAGES[state["page"]][1])
    heading <= title
    heading <= element("span", "PYTHON / BROWSER", "pill")
    parent <= heading
    PAGES[state["page"]][2](parent)
    if not storage_ok:
        notify("Browser storage is unavailable. Export a backup before closing this page.", True)


load()
reset_simulation()
render()
