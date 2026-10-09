import { readFile } from "node:fs/promises";
import { CircuitEngine } from "./circuit.mjs";
const [circuitPath, readingsPath] = process.argv.slice(2);
if (!circuitPath || !readingsPath)
  throw new Error("usage: node src/cli.mjs circuit.json inputs.json");
const circuit = new CircuitEngine(
  JSON.parse(await readFile(circuitPath, "utf8")),
);
const readings = JSON.parse(await readFile(readingsPath, "utf8"));
if (!Array.isArray(readings) || readings.length > 100000)
  throw new Error("bounded input array required");
const events = readings.map((row) => circuit.scan(row.inputs, row.timestampMs));
console.log(
  JSON.stringify({ scans: events.length, final: events.at(-1), events }),
);
