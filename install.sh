#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/shadow_mirror"
BIN_DIR="${HOME}/.local/bin"
VENV_DIR="${PROJECT_DIR}/venv"

python3 -m venv "$VENV_DIR"
"${VENV_DIR}/bin/pip" install -r "${PROJECT_DIR}/requirements.txt"
mkdir -p "$CONFIG_DIR" "$BIN_DIR"

if [[ ! -f "${CONFIG_DIR}/.env" ]]; then
    cp "${PROJECT_DIR}/.env.example" "${CONFIG_DIR}/.env"
fi

ln -sf "${PROJECT_DIR}/bin/shadow-mirror" "${BIN_DIR}/shadow-mirror"
echo "Installed. Next: add OPENROUTER_API_KEY to ${CONFIG_DIR}/.env, then run shadow-mirror --entry."
