import argparse
import json
from pathlib import Path

from .engine import CircuitEngine
from .structured_text import structured_text


def main():
    parser = argparse.ArgumentParser(description="Electrical control simulation and PLC export")
    sub = parser.add_subparsers(dest="command", required=True)
    simulate = sub.add_parser("simulate")
    simulate.add_argument("circuit")
    simulate.add_argument("inputs")
    export = sub.add_parser("export-plc")
    export.add_argument("circuit")
    export.add_argument("--name", default="BrunnoCircuit")
    args = parser.parse_args()
    try:
        definition = json.loads(Path(args.circuit).read_text(encoding="utf-8"))
        if args.command == "export-plc":
            print(structured_text(definition, args.name), end="")
        else:
            engine = CircuitEngine(definition)
            events = json.loads(Path(args.inputs).read_text(encoding="utf-8"))
            results = [engine.scan(event["inputs"], event.get("timestampMs", event.get("atMs"))) for event in events]
            print(json.dumps({"scans": len(results), "events": results}, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, str(error) + "\n")


if __name__ == "__main__":
    main()
