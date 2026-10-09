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

## Optional report archive

Export a JSON report from the command above, then run `python cloud/sync.py enqueue result.json --project eletrical-comands-and-teory` and `python cloud/sync.py sync`. Synchronization requires `BRUNNODEV_ACCESS_TOKEN` and the external operations API; the local outbox retains unacknowledged reports.

## License

Original source and documentation are MIT licensed; see [LICENSE](LICENSE). Third-party dependencies and media retain their respective terms. Maintained by [Brunno Dev](https://brunnodev.store).
