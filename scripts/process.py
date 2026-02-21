#!/usr/bin/env python3
import os
import sys
import csv
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

def main():
    if len(sys.argv) < 3:
        print("Usage: process.py <timestamp> <spoons_level>")
        sys.exit(1)

    timestamp = sys.argv[1]
    spoons = sys.argv[2]
    
    # Setup Paths
    config_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "shadow_mirror"
    raw_dir = config_dir / "raw"
    synthesis_dir = config_dir / "synthesis"
    data_dir = config_dir / "data"
    
    raw_file = raw_dir / f"entry_{timestamp}.txt"
    synth_file = synthesis_dir / f"entry_{timestamp}.md"
    csv_file = data_dir / "entries.csv"

    # Load environment variables
    env_path = config_dir / ".env"
    load_dotenv(dotenv_path=env_path)

    # Require OpenRouter API Key
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print(f"Error: OPENROUTER_API_KEY not found in {env_path}")
        sys.exit(1)
        
    model_name = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o")

    # Initialize client pointing to OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # 1. Read Raw Text (written by shadow-mirror)
    try:
        with open(raw_file, "r") as f:
            raw_text = f.read().strip()
    except Exception as e:
        print(f"Error reading raw text file: {e}")
        sys.exit(1)

    if not raw_text:
        print("Error: Empty input text. Aborting.")
        sys.exit(1)

    # 2. Synthesis (Hegelian Dialectic)
    print(f"[{timestamp}] Generating synthesis...")
    
    system_prompt = """
You are the Jungian Mirror Engine. The user is providing a raw, unfiltered thought dump, likely recorded during a period of cognitive fog or emotional activation.

Your task is to structure this raw input using a Hegelian Dialectic:
1. **Thesis:** Summarize the user's stated trigger, emotion, or problem exactly as they feel it. No judgment.
2. **Antithesis:** Identify the projected shadow, unacknowledged insecurity, or alternative perspective. What is the hidden loop or fear driving the thesis?
3. **Synthesis:** Provide a compassionate, actionable integration. How can the user hold both the thesis and antithesis without guilt?

Important: At the very top of your response, provide a 3-5 word summary of the trigger prefixed EXACTLY with "TRIGGER_SUMMARY: ". Then provide the rest of the synthesis in Markdown.
"""

    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_text}
            ],
            temperature=0.7
        )
        synthesis_text = completion.choices[0].message.content
    except Exception as e:
        print(f"Error during synthesis: {e}")
        sys.exit(1)

    # Parse out the trigger summary
    trigger_summary = "Transcription processed."
    final_synthesis = []
    for line in synthesis_text.split("\n"):
        if line.startswith("TRIGGER_SUMMARY:"):
            trigger_summary = line.replace("TRIGGER_SUMMARY:", "").strip()
        else:
            final_synthesis.append(line)
    
    synthesis_text = "\n".join(final_synthesis).strip()

    # Save Synthesis
    try:
        with open(synth_file, "w") as f:
            f.write(synthesis_text)
    except OSError as e:
        print(f"Error writing synthesis: {e}")
        sys.exit(1)

    # 3. Append to CSV
    # format: timestamp,spoons,trigger_summary
    file_exists = csv_file.exists()
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "spoons", "trigger_summary"])
        writer.writerow([timestamp, spoons, trigger_summary])

    print(f"[{timestamp}] Processing complete! Spoons: {spoons}")
    print(f"Synthesis saved to: {synth_file}")

if __name__ == "__main__":
    main()
