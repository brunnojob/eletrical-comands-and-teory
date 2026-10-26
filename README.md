# Electrical Controls Lab

Electrical control simulation and automation logic in Python.

**[Open the lab](https://brunnojob.github.io/eletrical-comands-and-teory/)** · [Original website](https://comandoeletricobrunno.netlify.app/)

- Six simulators: DOL, reversal, star-delta, traffic lights, phase failure and VFD.
- Motor calculations, virtual multimeter, theory, training and project planning.
- Circuit editor, scan history, interlocks, TON timers and PLC Structured Text export.
- Projects and progress saved in browser storage. JSON backup and legacy project import.

No login, API token or backend. Python runs through Brython; HTML and CSS provide the interface. The browser downloads the pinned runtime from jsDelivr. Data stays on the current browser and site address; export a backup to move it.

## Run locally

Requires Python 3.11+; no Python dependencies.

```sh
python -m http.server 8000
```

Open `http://localhost:8000`. Internet access is needed to load Brython.

```sh
python -m electrical simulate examples/seal-in.json examples/inputs.json
python -m electrical export-plc examples/seal-in.json
python -m unittest discover -s tests -v
```

GitHub Actions tests the Python code and publishes the browser app to GitHub Pages.

Learning simulator only; it does not operate physical equipment. Sizing outputs are study estimates.

[MIT License](LICENSE) · [Brunno Dev](https://github.com/brunnojob) · [Sponsor](https://buymeacoffee.com/brunnodev)
