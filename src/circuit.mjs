export class CircuitEngine {
  constructor(definition) {
    if (
      !definition ||
      !Array.isArray(definition.coils) ||
      definition.coils.length > 128
    )
      throw new Error("invalid_circuit");
    this.coils = new Map();
    this.timers = new Map();
    this.sequence = 0;
    this.previousTime = -1;
    this.definition = structuredClone(definition);
    for (const coil of this.definition.coils) {
      if (
        !coil.id ||
        this.coils.has(coil.id) ||
        !/^[A-Z][A-Z0-9_]{0,31}$/.test(coil.id)
      )
        throw new Error("duplicate_or_invalid_coil");
      this.coils.set(coil.id, false);
      this.validate(coil.logic, 0);
    }
    this.interlocks = this.definition.interlocks ?? [];
    for (const group of this.interlocks)
      if (
        !Array.isArray(group) ||
        group.length < 2 ||
        group.some((id) => !this.coils.has(id))
      )
        throw new Error("invalid_interlock");
  }
  validate(node, depth) {
    if (!node || typeof node !== "object" || depth > 32)
      throw new Error("invalid_logic_tree");
    if (node.type === "contact") {
      if (typeof node.signal !== "string" || !["NO", "NC"].includes(node.mode))
        throw new Error("invalid_contact");
    } else if (["and", "or"].includes(node.type)) {
      if (
        !Array.isArray(node.children) ||
        node.children.length < 1 ||
        node.children.length > 128
      )
        throw new Error("invalid_gate");
      node.children.forEach((child) => this.validate(child, depth + 1));
    } else if (node.type === "ton") {
      if (
        !/^[A-Z][A-Z0-9_]{0,31}$/.test(node.id) ||
        !Number.isFinite(node.delayMs) ||
        node.delayMs < 0 ||
        node.delayMs > 3600000 ||
        this.timers.has(node.id)
      )
        throw new Error("invalid_timer");
      this.timers.set(node.id, { since: null });
      this.validate(node.input, depth + 1);
    } else throw new Error("unknown_node_type");
  }
  evaluate(node, inputs, prior, now) {
    if (node.type === "contact") {
      const value = Object.hasOwn(inputs, node.signal)
        ? inputs[node.signal]
        : prior.get(node.signal);
      if (typeof value !== "boolean")
        throw new Error(`missing_signal:${node.signal}`);
      return node.mode === "NO" ? value : !value;
    }
    if (node.type === "and" || node.type === "or") {
      const values = node.children.map((child) =>
        this.evaluate(child, inputs, prior, now),
      );
      return node.type === "and" ? values.every(Boolean) : values.some(Boolean);
    }
    const timer = this.timers.get(node.id);
    if (!this.evaluate(node.input, inputs, prior, now)) {
      timer.since = null;
      return false;
    }
    timer.since ??= now;
    return now - timer.since >= node.delayMs;
  }
  scan(inputs, now) {
    if (!Number.isSafeInteger(now) || now < 0 || now <= this.previousTime)
      throw new Error("non_monotonic_scan_time");
    if (
      !inputs ||
      Object.values(inputs).some((value) => typeof value !== "boolean") ||
      Object.keys(inputs).some((key) => this.coils.has(key))
    )
      throw new Error("invalid_inputs");
    const prior = new Map(this.coils);
    const timerSnapshot = structuredClone([...this.timers]);
    const next = new Map();
    try {
      for (const coil of this.definition.coils)
        next.set(coil.id, this.evaluate(coil.logic, inputs, prior, now));
      const conflicts = this.interlocks.filter(
        (group) => group.filter((id) => next.get(id)).length > 1,
      );
      for (const group of conflicts) group.forEach((id) => next.set(id, false));
      this.coils = next;
      this.previousTime = now;
      this.sequence++;
      return {
        sequence: this.sequence,
        timestampMs: now,
        coils: Object.fromEntries(next),
        transitions: [...next]
          .filter(([id, value]) => prior.get(id) !== value)
          .map(([id, value]) => ({ id, energized: value })),
        interlockTrips: conflicts,
      };
    } catch (error) {
      this.timers = new Map(timerSnapshot);
      throw error;
    }
  }
}
