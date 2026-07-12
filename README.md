# **Shadow Mirror 🪞**

**An AI-mediated Jungian shadow integration system, built explicitly for users with chronic illness and brain fog.**

## **BLUF**

Deep psychological growth requires immense working memory and sustained focus—resources often unavailable during cognitive fatigue or chronic illness flares. **Shadow Mirror** acts as a collaborative cognitive prosthesis. The user provides raw, unfiltered, voice-first emotional dumps; the AI provides the Hegelian dialectic structure and Jungian mirroring.

_Zero judgment. Zero pressure. Designed for finite energy._

## **🛠 Core Architecture**

This project is a local, terminal-native tool based in `~/.config/shadow_mirror/`.

- **Frontend:** Bash/CLI (pure `read`/`echo`, with optional `fzf` for frictionless selection)
- **Data Storage:** Flat text/markdown files and CSVs within `~/.config/shadow_mirror/data/`. Auth is handled implicitly by the local `$USER` environment.
- **Processing:** Shell scripts orchestrating lightweight Python API wrappers for OpenRouter-compatible LLMs (Hegelian Synthesis).

### **The 3 Pillars of the System**

1. **The Fog-Proof Input Pipeline:** Voice-first capture. Bypasses the resistance and fine-motor requirements of typing. Tolerates fragmented speech and pauses.
2. **The Mirror Engine:** Structures raw thought dumps using a Hegelian Dialectic (Thesis \-\> Antithesis \-\> Synthesis). Cross-references past entries to identify psychological loops.
3. **Energy-Gated UI:** Interface density adapts to the user's declared energy level ("Spoons").
   - _Red Days:_ Input only. Complex insights are locked to prevent overload.
   - _Yellow Days:_ Bite-sized summaries.
   - _Green Days:_ Full dialectic breakdown and historical pattern review.

## **🛑 Development Guardrails (The "Constraint-to-Catalyst" Philosophy)**

If you are contributing to or developing this repository, you must adhere to the following constraints. **Do not merge code that violates the Fog Test.**

1. **The Fog Test:** A user in a severe fatigue crash must be able to open the app, log an emotional trigger via voice, and close it in under 30 seconds.
2. **Zero Judgment UI:** No gamification, no streaks, no red alert badges. Guilt drains energy. The app is a passive, waiting mirror.
3. **Asynchronous Processing:** The user should never have to wait staring at a loading spinner for heavy psychological insights. Input is immediate; processing happens in the background.

## Install

```bash
git clone https://github.com/ryan258/shadow_mirror.git shadow_mirror
cd shadow_mirror
./install.sh
```

Add your key to `~/.config/shadow_mirror/.env`. Ensure `~/.local/bin` is on your `PATH`, then use the commands below.

| Command | Description |
| --- | --- |
| `shadow-mirror --entry` | Capture a thought and start background synthesis. |
| `shadow-mirror --review` | Review a past synthesis. |
| `shadow-mirror --patterns` | On a Green day, name up to three recurring themes. |
| `shadow-mirror --status` | See mirrored, processing, and retryable entries. |
| `shadow-mirror --retry` | Re-mirror failed entries in the background. |

## Privacy mode

To use an OpenAI-compatible local server such as Ollama, set these values in `~/.config/shadow_mirror/.env`:

```dotenv
OPENROUTER_API_KEY=ollama
OPENROUTER_BASE_URL=http://localhost:11434/v1
OPENROUTER_MODEL=llama3.1
```

The default base URL remains OpenRouter. The API key value only needs to be non-empty for local servers that do not require authentication.

## **🗺 Documentation Map**

Before modifying this codebase, please review the foundational documents:

- [BRIEF.md](./BRIEF.md): The comprehensive project specification and problem/solution mapping.
- [ROADMAP.md](./ROADMAP.md): The 12-week MVP execution plan.
- [GEMINI.md](./GEMINI.md): The persistent system context for AI CLI agents (e.g., Gemini, Cursor, Antigravity) to prevent architectural bloat and maintain MS-aware constraints.

_“I didn't choose this. I chose to keep creating anyway.”_
