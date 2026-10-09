# Electrical Circuit Engine

A circuit interpreter with NO/NC contacts, AND/OR logic, TON timing, previous-state latching, and mutually exclusive coils.

## Run

Requirements: Node.js 24.

```sh
npm test
node src/cli.mjs examples/seal-in.json examples/inputs.json > result.json
```

## Behavior

Configuration bounds expression depth, tags, and coils. The clock cannot move backward. Invalid inputs do not change committed timers. Tests cover latching, delays, and interlocks.

## Result synchronization

The [operations archive](https://vercel-home-telemetry-api.vercel.app/laboratory.html?project=eletrical-comands-and-teory) stores execution results. Supabase migrations are in the [API repository](https://github.com/brunnojob/vercel-home-telemetry-api/tree/main/supabase/migrations).

```sh
python cloud/sync.py enqueue result.json --project eletrical-comands-and-teory
python cloud/sync.py sync
```

Set `BRUNNODEV_ACCESS_TOKEN` to your session token. The SQLite outbox retains reports until the server confirms persistence; identical content does not create duplicate records. Tokens are not stored in source code. To run the synchronization tests:

```sh
python -m unittest discover -s cloud
```
