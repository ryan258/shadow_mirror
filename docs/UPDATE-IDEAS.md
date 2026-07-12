# UPDATE-IDEAS: Shadow Mirror Review & Improvement Proposals

**Date:** 2026-07-11
**Filter applied:** Every proposal was checked against the Fog Test, Zero Judgment UI, and async-latency rules. Completed work is retained here as a checked-off record and detailed in [changelog.md](../changelog.md).

---

## BLUF

P0, P1, and P2 are complete. The tool now has reliable background processing, loop-aware synthesis and review, a simple installation path, local-model support, and a documented flat-file data contract. P3 remains deliberately deferred until real use demonstrates the need.

## Completed

### P0 — Correctness & Trust

- [x] **0.1 Silent background failure** — markers, `--status`, and calm entry-time notice.
- [x] **0.2 No retry path for failed syntheses** — background `--retry` command.
- [x] **0.3 Portable script resolution** — supports macOS and symlinked installation paths.
- [x] **0.4 Optional `fzf`** — review falls back to the newest synthesis in `$PAGER`.
- [x] **0.5 Interrupted entry capture** — Ctrl+C preserves and processes partial input.
- [x] **0.6 API timeout** — 120-second timeout with two retries.
- [x] **0.7 Tolerant trigger-summary parsing** — accepts common markdown wrappers.

### P1 — Pattern Recognition

- [x] **1.1 Loop-aware synthesis** — last 20 trigger summaries provide reference-only context.
- [x] **1.2 Green-day pattern surfacing** — `--patterns` names up to three recurring themes.

### P2 — Adoption & Professional Polish

- [x] **2.1 Installation path** — `requirements.txt`, `.env.example`, `install.sh`, and README instructions.
- [x] **2.2 External system prompt** — operator-editable `prompt.md` seeded from `prompts/synthesis.md`.
- [x] **2.3 Local/private model support** — configurable OpenAI-compatible base URL and Privacy Mode docs.
- [x] **2.4 Red-day language** — holding-mirror message replaces denial framing.
- [x] **2.5 ShellCheck and processor smoke test** — clean lint plus stdlib regression coverage.
- [x] **2.6 Data contract** — telemetry header and [DATA-FORMAT.md](DATA-FORMAT.md).
- [x] **2.7 Unused audio scaffold** — removed in favor of OS-level dictation input.

---

## P3 — Optional Depth (dogfood before starting)

### 3.1 MCP server for the entry archive

Expose the synthesis archive as a read-only MCP server (`search_entries`, `get_entry`, `get_trigger_history`) so the operator's own agent sessions can reference shadow-work history.

**Hold because:** it serves an audience beyond the operator. Add only once core usage is established.

### 3.2 Weekly digest (`--digest`)

One LLM call over a week's syntheses producing a five-line Markdown digest. Add only if `--patterns` proves insufficient.

### 3.3 Semantic search over syntheses

Embeddings plus a local vector index. Defer until full-text review demonstrably fails on a real archive.

---

## Rejected (do not resurrect without new evidence)

| Idea | Why rejected |
| --- | --- |
| TUI dashboard (charts, spoons trends) | Fails Fog Test and Zero Judgment — trend lines become guilt metrics. |
| Streak / consistency tracking | Explicitly banned by Zero Judgment UI. |
| Desktop notifications when synthesis completes | An interruption engine pointed at someone managing energy. |
| Web UI / mobile app | Architecture explicitly forbids web frameworks; terminal-native is the identity. |
| Direct in-tool audio recording (`ffmpeg` + Whisper API) | Superwhisper already solves capture better at the OS layer. |
| Multi-user support / cloud sync | Single-operator local tool by design; auth is the `$USER` session. |
| Interactive config wizard | Violates the no-interactive-auth rule; `.env.example` and `install.sh` cover setup. |

_"I didn't choose this. I chose to keep creating anyway."_
