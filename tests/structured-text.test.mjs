import test from "node:test";
import assert from "node:assert/strict";
import { structuredText } from "../src/structured-text.mjs";

test("internal PLC names never collide with declared signals", () => {
  const text = structuredText({ coils: [{ id: "P0", logic: { type: "contact", signal: "N0", mode: "NO" } }] });
  assert.match(text, /P1 := P0;/);
  assert.match(text, /N1 := N0;/);
  assert.throws(() => structuredText({ coils: [{ id: "AND", logic: { type: "contact", signal: "S", mode: "NO" } }] }));
});

test("feedback uses the previous scan and commits outputs after interlocks", () => {
  const text = structuredText({ coils: [
    { id: "MOTOR", logic: { type: "or", children: [
      { type: "contact", signal: "START", mode: "NO" },
      { type: "contact", signal: "MOTOR", mode: "NO" },
    ] } },
    { id: "REVERSE", logic: { type: "contact", signal: "BACK", mode: "NO" } },
  ], interlocks: [["MOTOR", "REVERSE"]] });
  assert.match(text, /P0 := MOTOR;/);
  assert.match(text, /N0 := \(START OR P0\);/);
  assert.ok(text.indexOf("BOOL_TO_INT") < text.indexOf("MOTOR := N0"));
  assert.equal(text.match(/MOTOR : BOOL;/g).length, 1);
});

test("nested TON blocks execute their inputs before their parent", () => {
  const text = structuredText({ coils: [{ id: "MOTOR", logic: {
    type: "ton", id: "OUTER", delayMs: 2000, input: {
      type: "ton", id: "INNER", delayMs: 100, input: { type: "contact", signal: "START", mode: "NO" },
    },
  } }] });
  assert.ok(text.indexOf("T0(IN := START") < text.indexOf("T1(IN := T0.Q"));
  assert.match(text, /PT := T#2000ms/);
});

test("rejects invalid identifiers and timer precision instead of emitting broken PLC code", () => {
  assert.throws(() => structuredText({ coils: [] }, "bad;code"));
  assert.throws(() => structuredText({ coils: [{ id: "M", logic: { type: "ton", id: "T", delayMs: 0.5,
    input: { type: "contact", signal: "S", mode: "NO" } } }] }));
});
