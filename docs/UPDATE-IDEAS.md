# UPDATE-IDEAS: Shadow Mirror Review & Improvement Proposals

**Date:** 2026-07-11
**Scope reviewed:** `bin/shadow-mirror` (165 lines), `scripts/process.py` (117 lines), all project docs.
**Filter applied:** Every proposal below was checked against the Fog Test, Zero Judgment UI, and async-latency rules. Ideas that failed are listed at the bottom in "Rejected" — keeping them visible prevents re-litigating them later.

---

## BLUF

The first trust-and-core sitting is shipped: background failures are visible and retryable, API calls are bounded, past triggers inform syntheses, and the Red-day gate is consistent with Zero Judgment. The remaining proposals are intentionally deferred until they earn their complexity.

Priority order: **P0 = bugs/trust, P1 = the missing core feature, P2 = adoption & professional polish, P3 = optional depth.**

---

## Completed

- [x] **0.1 Silent background failure** — failure markers, `--status`, and a calm entry-time notice.
- [x] **0.2 No retry path for failed syntheses** — background `--retry` command.
- [x] **0.6 No timeout on the API call** — 120-second timeout with two retries.
- [x] **1.1 Cross-referencing past entries** — last 20 trigger summaries provide loop context.
- [x] **2.4 Soften the Red-day review message** — replaced judgmental denial framing.

Implementation details: [changelog.md](../changelog.md).

---

## P0 — Correctness & Trust (fix before anything else)

### 0.3 Dead `readlink` fallback / macOS breakage

**Problem:** `command -v readlink` succeeds on every macOS, so the fallback branch for "old macOS without GNU readlink" is unreachable. On macOS < 12.3, `readlink -f` fails, and under `set -e` the script dies mid-entry — after the user has already spoken their entry.

**Proposal:** Replace the whole block with the portable idiom:

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```

Symlink resolution is only needed if the binary is symlinked into `PATH`; if so, use `readlink "${BASH_SOURCE[0]}" 2>/dev/null || echo "${BASH_SOURCE[0]}"` (plain `readlink`, no `-f`, works everywhere).

**Effort:** Trivial.

### 0.4 Unchecked hard dependency on `fzf`

**Problem:** `--review` pipes into `fzf` without checking it exists. Missing `fzf` + `set -eo pipefail` = cryptic crash on a Green day, exactly when the user finally has energy to review.

**Proposal:** Guard it: if `fzf` is absent, fall back to `ls -t` the five most recent synthesis files and open the newest in `${PAGER:-less}`. Degraded but functional beats dead.

**Effort:** Small.

### 0.5 Interrupted entry leaves a partial file

**Problem:** If the user hits Ctrl+C instead of Ctrl+D during `cat > "$raw_file"` (a very fog-plausible mistake), `set -e` kills the script and a partial raw file is stranded — it will never be processed and never flagged.

**Proposal:** `trap` INT during capture: on interrupt, keep the partial file (never discard words the user spoke), print `"Entry saved as-is."`, and hand off to processing normally. The mirror should treat Ctrl+C and Ctrl+D identically.

**Effort:** Small.

### 0.7 Fragile `TRIGGER_SUMMARY:` parsing

**Problem:** The trigger summary is extracted by scanning for a magic prefix the LLM is merely *asked* to emit. Weaker/local models routinely bold it, prefix it, or omit it — silently degrading `entries.csv` (every row becomes "Transcription processed.").

**Proposal (lazy):** Make the scan case-insensitive and tolerant of leading `#`/`*` markdown, and strip surrounding `**`. ~4 lines.
**Proposal (robust, only if lazy version proves insufficient):** Two-message approach or JSON mode via OpenRouter's `response_format`. Defer until the lazy fix demonstrably fails.

**Effort:** Trivial → Small.

---

## P1 — Pattern Recognition Follow-up

### 1.2 Loop surfacing on Green days

**Problem:** Even with 1.1, loops are buried inside individual synthesis files.

**Proposal:** `shadow-mirror --patterns` (Green days only, reuse the existing spoons gate): send the full `entries.csv` trigger column to the LLM with a "name the 3 most recurrent themes, one line each" prompt, print the result, done. No caching, no state — the CSV is tiny for years of daily use.

**Effort:** Small.

---

## P2 — Adoption & Professional Polish

This is what makes the project legible and installable for AI professionals. Right now nobody but the author can run it.

### 2.1 Installation path

**Problem:** No `requirements.txt`, no `.env.example`, no install instructions. The venv is committed-adjacent (in-tree, gitignored) and the Bash script hardcodes its location relative to the repo.

**Proposal:**
- `requirements.txt` with two lines: `openai`, `python-dotenv`.
- `.env.example` with `OPENROUTER_API_KEY=` and `OPENROUTER_MODEL=openai/gpt-4o`.
- `install.sh` (~20 lines): create venv, pip install, symlink `bin/shadow-mirror` into `~/.local/bin`, create `~/.config/shadow_mirror/`, copy `.env.example` if no `.env` exists, print exactly one next step.
- A short "Install" section in README (3 commands).

**Effort:** Small. **Payoff:** the difference between a gist and a tool.

### 2.2 Externalize the system prompt

**Problem:** The Hegelian dialectic prompt is a string literal inside `process.py`. For AI professionals, the prompt *is* the product — they'll want to read it, tune it, and version their variants without touching code.

**Proposal:** Move it to `~/.config/shadow_mirror/prompt.md`, seeded from a `prompts/synthesis.md` in the repo on first run. `process.py` reads the file; if missing, writes the default. ~6 lines changed.

**Effort:** Small.

### 2.3 Local/private model support (Ollama)

**Problem:** This tool handles the most sensitive data a person produces. Many AI professionals will refuse to send shadow-work transcripts to a cloud API — and they're right to hesitate.

**Proposal:** No new code needed, only configuration: the OpenAI client already accepts a custom `base_url`. Add `OPENROUTER_BASE_URL` (default `https://openrouter.ai/api/v1`) to the env handling — pointing it at `http://localhost:11434/v1` with `OPENROUTER_MODEL=llama3.1` makes it fully local. Document it as a first-class "Privacy Mode" section in the README. ~3 lines of code, big trust signal.

**Effort:** Trivial. **Payoff:** the single strongest credibility feature for this audience.

### 2.5 Shellcheck + one smoke test

**Problem:** No tests, no lint. For a Bash-centric project pitching "defensive Bash" as a value, that's a credibility gap.

**Proposal:**
- Run `shellcheck bin/shadow-mirror` once and fix what it flags (the `local x=$(cmd)` exit-status masking on lines 53, 61, 117, 131 will be its first complaints).
- One `test_process.py` that runs `process.py` against a stub raw file with a fake `base_url` pointing at a 5-line stdlib `http.server` mock — asserts the synthesis file and CSV row get written. No pytest fixtures, no framework beyond `assert`.
- Optional: a 6-line GitHub Actions workflow running both.

**Effort:** Small.

### 2.6 Header for `telemetry.csv` + document the data contract

**Problem:** `telemetry.csv` has no header row; `entries.csv` does. The flat-file schema — the most reusable idea in the project — is undocumented.

**Proposal:** Add the header write-once pattern to `log_telemetry` (same as `process.py` does), and add a `docs/DATA-FORMAT.md` page (half a page: the four directories, the two CSVs, the file naming convention). AI professionals evaluating "flat files as a memory substrate" will read exactly this page.

**Effort:** Trivial.

### 2.7 Remove or use the `audio/` directory

**Problem:** `audio/` is created but never written to. The Whisper-direct pipeline from BRIEF.md was (sensibly) replaced by Superwhisper paste. Dead scaffolding contradicts the project's own minimalism.

**Proposal:** Delete `AUDIO_DIR` from the script and strike direct-Whisper references from BRIEF.md. If direct audio capture is ever wanted, it re-enters through the Rejected list below with its own justification.

**Effort:** Trivial.

---

## P3 — Optional Depth (only after P0–P2 are done and dogfooded)

### 3.1 MCP server for the entry archive

**Concept:** Expose the synthesis archive as a read-only MCP server (`search_entries`, `get_entry`, `get_trigger_history`) so the user's own Claude/agent sessions can reference their shadow-work history. This is the feature that would make AI professionals *talk about* the project: a personal-psychology memory layer built on flat files.

**Constraint check:** Passes — it's read-only, adds no UI, and runs only when an agent asks. Implementation is ~80 lines with the official `mcp` Python SDK.

**Hold because:** It serves an audience beyond the operator. Ship it as `docs/MCP.md` + `scripts/mcp_server.py` only once the core is solid.

### 3.2 Weekly digest (`--digest`)

One LLM call over the week's syntheses producing a 5-line Markdown digest into `synthesis/weekly_<date>.md`. Green-day gated. Only add if `--patterns` (1.2) proves insufficient — they overlap heavily. YAGNI until dogfooding says otherwise.

### 3.3 Semantic search over syntheses

Embeddings + local vector index. **Deliberately deferred:** fzf full-text search over a few hundred small Markdown files is instant and fog-proof. Revisit only when the archive is large enough that fzf demonstrably fails to surface a known entry — likely years away.

---

## Rejected (fails the project's own constraints — do not resurrect without new evidence)

| Idea | Why rejected |
|------|--------------|
| TUI dashboard (charts, spoons trends) | Fails Fog Test and Zero Judgment — trend lines become guilt metrics. |
| Streak / consistency tracking | Explicitly banned by Zero Judgment UI. |
| Desktop notifications when synthesis completes | An interruption engine pointed at someone managing energy. `--status` (0.1) gives the same info, pull not push. |
| Web UI / mobile app | Architecture explicitly forbids web frameworks; terminal-native is the identity. |
| Direct in-tool audio recording (`ffmpeg` + Whisper API) | Superwhisper already solves capture better at the OS layer; would add a heavy dependency and a latency-critical foreground step. |
| Multi-user support / cloud sync | Single-operator local tool by design; auth is the `$USER` session. |
| Interactive config wizard | Violates the no-interactive-auth rule; `.env.example` + install.sh covers it. |

---

## Suggested execution order

1. Dogfood the completed trust and loop-aware changes.
2. **Remaining P0 batch** (0.3, 0.4, 0.5, 0.7): a focused second sitting.
3. Reassess **1.2** after observing whether loop-aware syntheses already surface enough value.
4. Add P2 adoption work only when there is a real publishing decision; dogfood before deciding on P3.

_"I didn't choose this. I chose to keep creating anyway."_
