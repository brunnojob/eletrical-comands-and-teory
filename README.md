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

Use the [shared operations archive client](https://github.com/brunnojob/vercel-home-telemetry-api/tree/main/cloud) to queue `result.json` under project `eletrical-comands-and-teory`. The client uses `BRUNNODEV_ACCESS_TOKEN` and retains unacknowledged reports locally.

## License

Original source and documentation are MIT licensed; see [LICENSE](LICENSE). Third-party dependencies and media retain their respective terms. Maintained by [Brunno Dev](https://brunnodev.store).
