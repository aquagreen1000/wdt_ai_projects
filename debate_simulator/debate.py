"""Debate orchestration and transcript generation."""

from .config import DEBATERS, TRANSCRIPT_FILE, TURNS_PER_DEBATER
from .evaluation import run_evaluation_phase
from .llm import call_ollama
from .prompts import build_prompt
from .turns import generate_turn_order


def run_debate(topic, transcript_file=TRANSCRIPT_FILE):
    """Run a debate for ``topic`` and save the Markdown transcript."""
    name_to_model = {debater["name"]: debater["model"] for debater in DEBATERS}
    debater_names = [debater["name"] for debater in DEBATERS]
    turn_order = generate_turn_order(debater_names, TURNS_PER_DEBATER)

    transcript_so_far = ""
    md_lines = [
        "# Debate Transcript",
        "",
        f"**Topic:** {topic}",
        "",
        "**Participants:**",
    ]
    for debater in DEBATERS:
        md_lines.append(f"- **{debater['name']}** - model: `{debater['model']}`")
    md_lines.extend(["", "---", ""])

    print(f"DEBATE TOPIC: {topic}\n" + ("=" * 60) + "\n")
    for turn_num, debater_name in enumerate(turn_order, start=1):
        model = name_to_model[debater_name]
        prompt = build_prompt(topic, debater_name, transcript_so_far)
        print(f"\n--- Turn {turn_num}: {debater_name} ({model}) is thinking... ---\n")

        response_text = call_ollama(model, prompt)
        print(f"[Turn {turn_num}] {debater_name}:\n{response_text}\n")

        md_lines.extend([
            f"## Turn {turn_num} - {debater_name}",
            "",
            f"*Model: `{model}`*",
            "",
        ])
        for paragraph in response_text.split("\n"):
            paragraph = paragraph.strip()
            if paragraph:
                md_lines.extend([paragraph, ""])
        md_lines.extend(["---", ""])
        transcript_so_far += f"\n{debater_name}: {response_text}\n"

    md_lines.extend([
        "## End of Debate",
        "",
        f"Total turns: {len(turn_order)} ({TURNS_PER_DEBATER} per debater, "
        f"{len(DEBATERS)} debaters).",
        "",
        "---",
        "",
    ])
    md_lines = run_evaluation_phase(topic, transcript_so_far, md_lines)

    with open(transcript_file, "w", encoding="utf-8") as transcript:
        transcript.write("\n".join(md_lines))
    print(f"\nDebate complete. Full transcript saved to '{transcript_file}'.")