# Shadow Mirror data format

All operator data lives under `~/.config/shadow_mirror/` (or `$XDG_CONFIG_HOME/shadow_mirror/`).

| Path | Contents |
| --- | --- |
| `raw/entry_<timestamp>.txt` | Original thought dump; never discarded after processing begins. |
| `synthesis/entry_<timestamp>.md` | The generated dialectic synthesis. |
| `data/entries.csv` | `timestamp,spoons,trigger_summary` for lightweight loop detection. |
| `logs/telemetry.csv` | `timestamp,action` for local command telemetry. |
| `logs/failed_<timestamp>` | Generic marker for a synthesis that can be re-mirrored. |
| `prompt.md` | Operator-editable synthesis prompt, seeded from `prompts/synthesis.md`. |

Timestamps use `YYYYMMDD_HHMMSS`. CSV fields are written with Python's standard CSV writer, so trigger summaries may safely contain commas.
