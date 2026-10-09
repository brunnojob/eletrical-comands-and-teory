import { readFile, writeFile } from "node:fs/promises";
import { structuredText } from "./structured-text.mjs";

const [source, destination, name] = process.argv.slice(2);
if (!source || !destination) throw new Error("usage: node src/export-plc.mjs CIRCUIT.json OUTPUT.st [BLOCK_NAME]");
const input = await readFile(source, "utf8");
if (Buffer.byteLength(input) > 262144) throw new Error("circuit_too_large");
await writeFile(destination, structuredText(JSON.parse(input), name));
