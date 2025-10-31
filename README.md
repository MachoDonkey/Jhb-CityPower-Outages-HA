# Jhb City Power Outages (Home Assistant custom integration)

This repository contains a Home Assistant custom integration scaffold for the Jhb City Power Outages service. It is prepared for HACS and includes a minimal working integration, config flow, tests, devcontainer, and CI.

Features in this scaffold
- Integration domain: `awesome_assistant` (internal domain used for the scaffold)
- Sensor platform using an async DataUpdateCoordinator that polls a (dummy) local endpoint
- Config flow for setting the affected area and scan interval
- Tests (pytest) with a minimal smoke test (skipped if Home Assistant isn't available in test env)
- Pre-commit, ruff, mypy configuration placeholders
- Devcontainer for Home Assistant development (integration blueprint style)
- CI workflow for linting, type checking and tests
- `hacs.json` for HACS metadata

Usage
1. Copy the `custom_components/awesome_assistant` folder to your Home Assistant `config/custom_components` folder (or install via HACS once published).
2. Restart Home Assistant.
3. Configure the integration via Settings -> Devices & Services -> Add Integration -> "Jhb City Power Outages" and provide the affected area and scan interval.

Notes
- This scaffold uses a dummy local endpoint (http://localhost:8080/outages) by default; swap it with the real City Power API in integration options later.
- The integration domain is currently `awesome_assistant` to match the scaffold template; this can be changed but must match `manifest.json` and the package folder name.
