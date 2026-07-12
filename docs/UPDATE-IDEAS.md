# UPDATE-IDEAS: Shadow Mirror Review & Improvement Proposals

**Date:** 2026-07-11
**Scope reviewed:** `bin/shadow-mirror` (165 lines), `scripts/process.py` (117 lines), all project docs.
**Filter applied:** Every proposal below was checked against the Fog Test, Zero Judgment UI, and async-latency rules. Ideas that failed are listed at the bottom in "Rejected" — keeping them visible prevents re-litigating them later.

---

## BLUF

The tool works, but it has one dangerous gap (silent background failures), one broken promise (pattern recognition is documented but not implemented), and zero onboarding path for anyone who isn't the original author. Fixing those three things — plus a handful of small hardening items — turns this from a personal script into a credible reference implementation of "constraint-driven AI tooling" that AI professionals can install, trust, and learn from.

Priority order: **P0 = bugs/trust, P1 = the missing core feature, P2 = adoption & professional polish, P3 = optional depth.**

---

## P0 — Correctness & Trust (fix before anything else)

### 0.1 Silent background failure

**Problem:** `record_entry` hands off to `process.py` via `nohup … &`. If the API key is missing, the network is down, or OpenRouter errors, the failure lands only in `process.log`. The user is told "Entry saved. Processing…" and never learns the synthesis was never written. For a tool whose whole promise is "the mirror is holding your thought safely," this is the worst possible failure mode.

**Proposal:** On failure, `process.py` writes a one-line marker file `${CONFIG_DIR}/logs/failed_<timestamp>` (raw text is already preserved in `raw/`, so nothing is lost). Add a `--status` command (~15 lines of Bash) that prints one calm line: how many entries are processed, pending, or need a retry. Also have `record_entry` check for failure markers at startup and mention them once, gently: `"1 earlier entry is waiting to be re-mirrored. Run: shadow-mirror --retry"`. No red text, no alarm.

**Effort:** Small. **Fog Test:** passes — status is one command, zero flags.

### 0.2 No retry path for failed syntheses

**Problem:** Raw text survives a failure, but there is no way to reprocess it short of manually invoking the venv Python with the right arguments — impossible under fog.

**Proposal:** `shadow-mirror --retry` loops over `failed_*` markers and re-launches `process.py` for each (background, same as entry). Spoons level can be re-read from `entries.csv` or default to "Yellow". ~10 lines.

**Effort:** Small.

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

### 0.6 No timeout on the API call

**Problem:** `client.chat.completions.create(...)` has no timeout. A hung connection leaves a zombie `nohup` process and an entry stuck in limbo forever.

**Proposal:** `client = OpenAI(..., timeout=120, max_retries=2)`. One line; the OpenAI SDK handles the rest. Combined with 0.1, a timeout becomes a visible, retryable failure.

**Effort:** Trivial.

### 0.7 Fragile `TRIGGER_SUMMARY:` parsing

**Problem:** The trigger summary is extracted by scanning for a magic prefix the LLM is merely *asked* to emit. Weaker/local models routinely bold it, prefix it, or omit it — silently degrading `entries.csv` (every row becomes "Transcription processed.").

**Proposal (lazy):** Make the scan case-insensitive and tolerant of leading `#`/`*` markdown, and strip surrounding `**`. ~4 lines.
**Proposal (robust, only if lazy version proves insufficient):** Two-message approach or JSON mode via OpenRouter's `response_format`. Defer until the lazy fix demonstrably fails.

**Effort:** Trivial → Small.

---

## P1 — The Missing Core Feature: Pattern Recognition

### 1.1 Cross-referencing past entries ("psychological loops")

**Problem:** README Pillar 2 promises: *"Cross-references past entries to identify psychological loops."* This is not implemented anywhere. Each synthesis is generated in isolation; `--review` is manual fzf search. This is the single biggest gap between what the docs claim and what the code does — and it's also the feature that makes the tool genuinely interesting to AI professionals (longitudinal memory in a flat-file system, no vector DB).

**Proposal (lazy, high leverage):** `entries.csv` already stores a trigger summary per entry. Before calling the LLM, `process.py` reads the last N (say 20) rows and appends them to the system prompt:

```
Recent trigger history (for loop detection only):
2026-07-02 (Yellow): fear of being replaced at work
2026-07-05 (Red): resentment toward partner's ease
...
If the current entry rhymes with a past trigger, name the loop gently in the Synthesis section.
```

~10 lines of Python, zero new dependencies, zero new storage. The LLM does the pattern matching — that's what it's good at, and the context cost of 20 five-word summaries is negligible.

**Effort:** Small. **Payoff:** the tool's flagship claim becomes true.

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

### 2.4 Soften the Red-day review message

**Problem:** `"🛑 Access Denied: Rest is required today."` violates the project's own Zero Judgment rule — a stop-sign emoji and the word "Denied" is exactly the red-alert framing CLAUDE.md bans.

**Proposal:** `"🪞 The mirror is holding everything safely. It will be here when you're rested."` Same gate, zero judgment.

**Effort:** Trivial.

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

1. **P0 batch** (0.1–0.7): one sitting, all small. Makes the tool trustworthy.
2. **1.1** loop-aware prompting: the flagship promise, ~10 lines.
3. **P2 batch** (2.1–2.7): makes it installable and credible. `install.sh` + privacy mode (2.3) are the highest-leverage items for the AI-professional audience.
4. Dogfood two weeks, then decide on P3 from real usage — per ROADMAP.md's own rule: the timeline is a framework, not a deadline.

_"I didn't choose this. I chose to keep creating anyway."_
