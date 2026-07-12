#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

mkdir -p "$TEMP_DIR/bin" "$TEMP_DIR/config/shadow_mirror/synthesis"
printf '#!/usr/bin/env bash\nexit 130\n' > "$TEMP_DIR/bin/fzf"
chmod +x "$TEMP_DIR/bin/fzf"
printf 'A synthesis.\n' > "$TEMP_DIR/config/shadow_mirror/synthesis/entry_20260711_180000.md"

printf '1' | PATH="$TEMP_DIR/bin:$PATH" XDG_CONFIG_HOME="$TEMP_DIR/config" PAGER=cat \
    "$PROJECT_DIR/bin/shadow-mirror" --review >/dev/null
