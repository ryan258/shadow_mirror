# **PROJECT BRIEF: Shadow Mirror**

## **BLUF (Bottom Line Up Front)**

**Shadow Mirror** is an AI-mediated Jungian shadow integration system built explicitly for users with chronic illness, limited cognitive bandwidth, and brain fog.

It solves a critical gap in psychological care: traditional therapy and deep introspection are often highly energy-prohibitive. This platform utilizes voice-first terminal input, AI scaffolding, and an energy-aware pacing system to make unconscious pattern-recognition accessible even during an MS crash.

**The Core Rule:** The system absorbs the cognitive load of structuring thought. The user provides the raw, unfiltered input; the AI provides the Hegelian dialectic structure and Jungian mirroring.

## **1\. The Problem & The "Constraint-to-Catalyst" Solution**

**The Problem:** Doing deep psychological growth work requires immense working memory and sustained focus—resources that are violently stripped away during cognitive fatigue or chronic illness flare-ups.

**The Solution:** Shadow Mirror acts as a collaborative cognitive prosthesis for psychological growth.

- **Voice-First, Fog-Optimized Input:** Bypasses the resistance and fine-motor requirements of typing. Captures raw, fragmented audio dumps via terminal commands.
- **Hegelian Dialectic Engine:** The Python/Bash processing pipeline structures raw input into Thesis (the trigger/emotion), Antithesis (the shadow element/projection), and Synthesis (the integration).
- **Asynchronous Mirroring:** Users do not need to process insights immediately. The system generates markdown files locally, holding the synthesized insights safely until the user has the "Spoons" (energy) to review them.

## **2\. Core Architecture**

Shadow Mirror operates as a dedicated, terminal-native environment located at `~/.config/shadow_mirror/`.

### **Module A: The Input Pipeline (Low-Friction Capture)**

- **CLI Text Interface:** Triggered via a simple bash command (`shadow-mirror --entry`). Bypasses typing by reading stdin from OS-level dictation tools (like Superwhisper).
- **API Parsing:** Calls external APIs (like OpenRouter) to semantically process the fragmented, brain-fogged speech into coherent emotional data points while saving compute resources locally.

### **Module B: The Integration Engine (Backend Shell/Python)**

- **Dialectic Processing:** Formats AI outputs into structured, digestible markdown files without overwhelming the user's terminal space.
- **Pattern Recognition:** Uses local CLI tools (`grep`, `fzf`) or lightweight Python scripts to cross-reference current inputs against the local `data/` directory to surface historical loops.

### **Module C: Energy-Gated CLI**

- **Capacity Checks:** The script prompts for current energy levels (Red/Yellow/Green) before dumping text to `stdout`.
- **Drip-Feed Integration:** Opens detailed markdown files only when capacity is high; suppresses output and operates silently when capacity is low.

## **3\. Guardrails & Development Philosophy**

Every feature merged into Shadow Mirror MUST adhere to these constraints:

1. **The Fog Test (User UX):** A user experiencing a severe MS crash must be able to open their terminal, run the command, log an emotional trigger via voice, and see the prompt return in under 30 seconds.
2. **Zero Judgment, Zero Pressure:** The interface must not use gamification, streaks, or red notifications. Guilt drains energy. The system is a passive, waiting mirror.
3. **Extreme Low Latency:** Utilize standard Bash builtins where possible and offload heavy AI processing to APIs to keep the local machine perfectly responsive.

## **4\. Phase 1: MVP Implementation Roadmap**

Based on the existing specification, the 12-week MVP targets the following sequence:

- **Week 1-2: Core Scaffolding.** Set up the `~/.config/shadow_mirror` directory structure and flat-file schema.
- **Week 3-5: The Voice Pipeline.** Implement high-fidelity audio transcription in Bash using `ffmpeg` and the Whisper API.
- **Week 6-8: The Mirroring Logic.** Prompt engineering and python API wrappers to perform the Hegelian Synthesis.
- **Week 9-11: Energy-Gated CLI.** Build the bash logic that adjusts `$stdout` density based on the user's declared energy level.
- **Week 12: Daily Use Validation.** Dogfood the tool daily to refine the frictionless workflow.

_“I didn't choose this. I chose to keep creating anyway.”_
