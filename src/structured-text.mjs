import { CircuitEngine } from "./circuit.mjs";

export function structuredText(definition, name = "BrunnoCircuit") {
  if (!/^[A-Za-z][A-Za-z0-9_]{0,31}$/.test(name)) throw new Error("invalid_block_name");
  const engine = new CircuitEngine(definition);
  const coils = [...engine.coils.keys()];
  const used = new Set([name.toUpperCase()]);
  const reserved = new Set("AND OR NOT XOR TRUE FALSE IF THEN ELSE ELSIF END_IF VAR VAR_INPUT VAR_OUTPUT END_VAR FUNCTION FUNCTION_BLOCK END_FUNCTION END_FUNCTION_BLOCK PROGRAM END_PROGRAM BOOL TON TIME INT REAL CASE OF END_CASE FOR TO DO END_FOR WHILE END_WHILE REPEAT UNTIL END_REPEAT RETURN".split(" "));
  function reserve(id) {
    if (reserved.has(id.toUpperCase()) || used.has(id.toUpperCase())) throw new Error("invalid_plc_identifier");
    used.add(id.toUpperCase());
  }
  for (const id of coils) reserve(id);
  function collect(node) {
    if (node.type === "contact") {
      if (!coils.includes(node.signal) && !used.has(node.signal.toUpperCase())) reserve(node.signal);
    } else if (node.children) node.children.forEach(collect);
    else collect(node.input);
  }
  engine.definition.coils.forEach(coil => collect(coil.logic));
  function allocate(prefix) {
    let i = 0;
    while (used.has(`${prefix}${i}`)) i += 1;
    const id = `${prefix}${i}`;
    used.add(id);
    return id;
  }
  const prior = new Map(coils.map(id => [id, allocate("P")]));
  const next = new Map(coils.map(id => [id, allocate("N")]));
  const inputs = new Set();
  const timers = new Map();
  const calls = [];
  function expression(node) {
    if (node.type === "contact") {
      if (!prior.has(node.signal)) inputs.add(node.signal);
      const value = prior.get(node.signal) ?? node.signal;
      return node.mode === "NO" ? value : `(NOT ${value})`;
    }
    if (node.type === "and" || node.type === "or")
      return `(${node.children.map(expression).join(node.type === "and" ? " AND " : " OR ")})`;
    if (!Number.isSafeInteger(node.delayMs)) throw new Error("integer_timer_delay_required");
    const input = expression(node.input);
    const id = allocate("T");
    timers.set(node.id, id);
    calls.push(`${id}(IN := ${input}, PT := T#${node.delayMs}ms);`);
    return `${id}.Q`;
  }
  const assignments = engine.definition.coils.map((coil) => `${next.get(coil.id)} := ${expression(coil.logic)};`);
  const lines = [`FUNCTION_BLOCK ${name}`];
  if (inputs.size) lines.push("VAR_INPUT", ...[...inputs].sort().map((id) => `  ${id} : BOOL;`), "END_VAR");
  if (coils.length) lines.push("VAR_OUTPUT", ...coils.map((id) => `  ${id} : BOOL;`), "END_VAR");
  const internal = [...prior.values(), ...next.values()];
  if (internal.length || timers.size)
    lines.push("VAR", ...internal.map((id) => `  ${id} : BOOL;`),
      ...[...timers.values()].map((id) => `  ${id} : TON;`), "END_VAR");
  lines.push(...coils.map((id) => `${prior.get(id)} := ${id};`), ...calls, ...assignments);
  for (const group of engine.interlocks) {
    lines.push(`IF (${group.map((id) => `BOOL_TO_INT(${next.get(id)})`).join(" + ")}) > 1 THEN`,
      ...group.map((id) => `  ${next.get(id)} := FALSE;`), "END_IF;");
  }
  lines.push(...coils.map((id) => `${id} := ${next.get(id)};`), "END_FUNCTION_BLOCK");
  return lines.join("\n") + "\n";
}
