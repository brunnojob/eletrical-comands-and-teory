# Electrical Controls Lab

Electrical control simulation and automation logic in Python.

**[Open the lab](https://brunnojob.github.io/eletrical-comands-and-teory/)**

- Complete English and Brazilian Portuguese interfaces, with light and dark themes. Language and theme preferences stay in the browser.
- Guided explanations and actual output changes at every step, including manual scans.
- 110, 220, 380, 440 and 660 V line-voltage presets.
- Sidebar symbol legend with names, terminal examples and technical references.
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

## Symbol references

The legend uses simplified educational drawings based on [IEC 60617](https://webstore.iec.ch/en/publication/2723), with the TON function block referenced to [IEC 61131-3](https://webstore.iec.ch/en/publication/68533). Auxiliary contact and coil terminal examples follow the [Schneider Electric device markings](https://www.se.com/us/en/faqs/FA110040/): 13–14 NO, 21–22 NC, A1–A2 coil. They are examples, not universal terminal assignments. Contacts are shown in their unactuated state. The main simulator diagram remains a conceptual control model, not a certified wiring drawing.
