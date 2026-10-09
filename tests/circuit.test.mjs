import test from "node:test";
import assert from "node:assert/strict";
import { CircuitEngine } from "../src/circuit.mjs";
const contact = (signal, mode = "NO") => ({ type: "contact", signal, mode });
test("seal-in circuit holds until stop and overload deenergize it", () => {
  const engine = new CircuitEngine({
    coils: [
      {
        id: "MOTOR",
        logic: {
          type: "and",
          children: [
            contact("STOP", "NC"),
            contact("OVERLOAD", "NC"),
            { type: "or", children: [contact("START"), contact("MOTOR")] },
          ],
        },
      },
    ],
  });
  const inputs = { START: true, STOP: false, OVERLOAD: false };
  assert.equal(engine.scan(inputs, 0).coils.MOTOR, true);
  assert.equal(engine.scan({ ...inputs, START: false }, 100).coils.MOTOR, true);
  assert.equal(
    engine.scan({ ...inputs, START: false, STOP: true }, 200).coils.MOTOR,
    false,
  );
});
test("mutually energized reversing coils trip the software interlock", () => {
  const engine = new CircuitEngine({
    coils: [
      { id: "FORWARD", logic: contact("F") },
      { id: "REVERSE", logic: contact("R") },
    ],
    interlocks: [["FORWARD", "REVERSE"]],
  });
  const result = engine.scan({ F: true, R: true }, 0);
  assert.equal(result.interlockTrips.length, 1);
  assert.equal(result.coils.FORWARD, false);
});
test("TON resets when its input falls", () => {
  const engine = new CircuitEngine({
    coils: [
      {
        id: "T",
        logic: { type: "ton", id: "T1", delayMs: 100, input: contact("START") },
      },
    ],
  });
  assert.equal(engine.scan({ START: true }, 0).coils.T, false);
  assert.equal(engine.scan({ START: true }, 100).coils.T, true);
  assert.equal(engine.scan({ START: false }, 200).coils.T, false);
  assert.equal(engine.scan({ START: true }, 300).coils.T, false);
});

test("rejects repeated members in an interlock", () => {
  assert.throws(() => new CircuitEngine({
    coils: [{ id: "PUMP", logic: contact("START") }],
    interlocks: [["PUMP", "PUMP"]],
  }), /invalid_interlock/);
});
test("rejects invalid contact identifiers before scanning", () => {
  assert.throws(() => new CircuitEngine({
    coils: [{ id: "PUMP", logic: contact("") }],
  }), /invalid_contact/);
});
