# Changelog

## 2026-07-11

### Added

- `shadow-mirror --status` reports mirrored, processing, and retryable entries in one calm line.
- `shadow-mirror --retry` re-launches failed entries in the background with a safe Yellow default.
- Syntheses receive the last 20 trigger summaries as reference-only context for gentle loop detection.
- `shadow-mirror --patterns` names up to three recurring themes on Green days.
- `install.sh`, `requirements.txt`, `.env.example`, and README instructions provide a minimal installation path.
- The system prompt is operator-editable at `~/.config/shadow_mirror/prompt.md`, seeded from `prompts/synthesis.md`.
- `OPENROUTER_BASE_URL` supports OpenAI-compatible local model servers such as Ollama.
- `docs/DATA-FORMAT.md` documents the flat-file storage contract.

### Fixed

- Processing failures now create generic `failed_<timestamp>` markers, including empty model responses, so failures remain visible and retryable.
- API calls now time out after 120 seconds and retry twice before becoming a visible failure.
- Script resolution now works through a symlinked installation without GNU `readlink`.
- Review remains functional without `fzf` by opening the newest synthesis in `$PAGER`.
- Ctrl+C during capture preserves and processes a partial thought.
- Markdown-wrapped `TRIGGER_SUMMARY` lines now populate trigger history correctly.
- `telemetry.csv` now receives a header row.

### Changed

- Red-day review now reassures the operator that the mirror is holding everything safely instead of denying access.
- Removed unused direct-audio scaffolding and documented OS-level dictation as the capture path.
