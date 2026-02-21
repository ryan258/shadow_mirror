# **SHADOW MIRROR: 12-Week MVP Development Roadmap**

## **BLUF**

This is the execution plan for the Shadow Mirror MVP. It operates as a local, terminal-native environment situated at `~/.config/shadow_mirror/`. The development process itself must follow the "Constraint-to-Catalyst" philosophy: build in small, high-signal bursts. **If your energy is Red, pause development.** The timeline is a framework, not a deadline.

## **Phase 1: Foundation & Data Structures (Weeks 1-2)**

**Goal:** Establish the directory scaffolding and core data structures.

- [x] **Initialize Local Environment:** Create `~/.config/shadow_mirror/` and subdirectories (`audio/`, `raw/`, `synthesis/`, `logs/`).
- [x] **Define Stack:** Pure Bash scripting for the UI/UX layer, orchestrating lightweight Python helpers for external APIs.
- [x] **Frictionless Auth:** None required. Operates implicitly on the local `$USER` session.
- [x] **Data Storage Design:**
  - `entries.csv`: Metadata registry (Dates, Spoons, Trigger Summary).
  - `raw/`: Raw text entries (pasted from Superwhisper).
  - `synthesis/`: Markdown files containing the AI-processed Hegelian dialectic.

## **Phase 2: The Fog-Proof Input Pipeline (Weeks 3-5)**

**Goal:** Build the terminal voice-first capture system using Superwhisper.

- [x] **CLI Capture:** `shadow-mirror --entry` command that reads piped/pasted text until EOF.
- [x] **OpenRouter Integration:** Python script to pull `OPENROUTER_API_KEY` from `~/.config/shadow_mirror/.env`.
- [x] **Raw Semantic Parsing:** Route the text to an LLM (e.g. `openai/gpt-4o`) to generate the Hegelian Synthesis.
- [x] **Self-Test (The Fog Test):** During a fatigue window, invoke the command, paste text via Superwhisper hotkey, and press `Ctrl+D`. The terminal must handle everything seamlessly.

## **Phase 3: The Mirror Engine / Backend AI (Weeks 6-8)**

**Goal:** Implement the Hegelian dialectic processing and Jungian pattern recognition via CLI commands.

- [x] **Prompt Engineering (Dialectic):** Develop the strict system prompt that forces the AI to output:
  - Thesis: The user's stated trigger.
  - Antithesis: The projected shadow or unacknowledged insecurity.
  - Synthesis: The actionable, compassionate integration.
- [x] **Pattern Recognition (grep/fzf):** Implement local file search utilizing grep/fzf or a lightweight semantic search script over the markdown files to identify psychological loops.
- [x] **Asynchronous Processing:** Run API calls in background subshells (`&`) so the terminal returns to the prompt immediately, notifying the user via a log or specific file when the synthesis is ready.

## **Phase 4: Energy-Gated CLI (Weeks 9-11)**

**Goal:** Build the terminal interface that actively protects the user when capacity is low.

- [x] **Energy Prompt:** An initial bash prompt upon invocation: `[1] Green, [2] Yellow, or [3] Red day?`
- [x] **State-Based Rendering:**
  - _Red Day:_ Script strictly limits output. Acknowledges receipt of voice input and exits immediately.
  - _Yellow Day:_ Prints a single, bite-sized paragraph summarizing past insights.
  - _Green Day:_ Opens `$EDITOR` or uses `fzf`/`less` to allow full review of dialectic breakdowns.

## **Phase 5: Refinement & Hardening (Week 12)**

**Goal:** Prove the constraint-to-catalyst hypothesis with daily usage.

- [x] **Onboarding Text:** Write a clean, zero-judgment terminal `shadow-mirror --help` output.
- [x] **Telemetry:** Keep a local `$XDG_STATE_HOME` or `logs/` file of session completions to track usability.
- [x] **Refine UX:** Polish the `read`/`echo` flows to minimize text clutter on the screen.

**Development Protocol Reminder:** Treat your own energy as finite. Use your triage system to determine if you have the capacity to build today.
