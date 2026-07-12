# Changelog

## 2026-07-11

### Added

- `shadow-mirror --status` reports mirrored, processing, and retryable entries in one calm line.
- `shadow-mirror --retry` re-launches failed entries in the background with a safe Yellow default.
- Syntheses receive the last 20 trigger summaries as reference-only context for gentle loop detection.

### Fixed

- Processing failures now create generic `failed_<timestamp>` markers, including empty model responses, so failures remain visible and retryable.
- API calls now time out after 120 seconds and retry twice before becoming a visible failure.

### Changed

- Red-day review now reassures the operator that the mirror is holding everything safely instead of denying access.
