#!/bin/bash
# Helper script to run Home Assistant inside the devcontainer.
# It expects the repository to be mounted at /workspace and a config mount at /config

set -euo pipefail

echo "Starting Home Assistant with config dir: /config"
exec python -m homeassistant --config /config
