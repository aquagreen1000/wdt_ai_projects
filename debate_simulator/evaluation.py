"""Peer evaluation and scorecard generation."""

from .config import DEBATERS
from .llm import call_ollama
from .prompts import build_evaluation_prompt


def parse_scores(response_text, expected_names):
    """Parse lines such as ``Debater Ben: 7`` into a score dictionary."""
    scores = {name: None for name in expected_names}
    for line in response_text.splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        name_part, score_part = line.rsplit(":", 1)
        name_part = name_part.strip()
        score_part = score_part.strip()

        for expected_name in expected_names:
            if expected_name.lower() in name_part.lower():
                digits = "".join(character for character in score_part if character.isdigit())
                if digits:
                    try:
                        scores[expected_name] = int(digits)
                    except ValueError:
                        pass
                break
    return scores


def run_evaluation_phase(topic, transcript_so_far, md_lines):
    debater_names = [debater["name"] for debater in DEBATERS]
    name_to_model = {debater["name"]: debater["model"] for debater in DEBATERS}

    print("\n" + "=" * 60)
    print("EVALUATION PHASE: debaters rate each other (1-10)")
    print("=" * 60 + "\n")

    results = {judge: {} for judge in debater_names}
    for judge_name in debater_names:
        other_names = [name for name in debater_names if name != judge_name]
        model = name_to_model[judge_name]
        prompt = build_evaluation_prompt(
            topic, judge_name, other_names, transcript_so_far
        )

        print(f"--- {judge_name} ({model}) is evaluating the other debaters... ---")
        response_text = call_ollama(model, prompt)
        print(f"{judge_name}'s raw evaluation:\n{response_text}\n")
        results[judge_name] = parse_scores(response_text, other_names)

    header_row = ["Debater \\ Judged by"] + debater_names + ["Average"]
    table_rows = []
    for ratee in debater_names:
        row = [ratee]
        collected_scores = []
        for judge in debater_names:
            if judge == ratee:
                row.append("-")
            else:
                score = results[judge].get(ratee)
                if score is not None:
                    row.append(str(score))
                    collected_scores.append(score)
                else:
                    row.append("N/A")
        average = (
            sum(collected_scores) / len(collected_scores)
            if collected_scores
            else None
        )
        row.append(f"{average:.2f}" if average is not None else "N/A")
        table_rows.append(row)

    print("\nFINAL EVALUATION RESULTS")
    print(" | ".join(header_row))
    for row in table_rows:
        print(" | ".join(row))

    md_lines.extend([
        "## Peer Evaluation Results",
        "",
        "Each debater rated the *other* debaters' arguments from 1 (worst) to 10 (best).",
        "",
        "| " + " | ".join(header_row) + " |",
        "|" + "|".join(["---"] * len(header_row)) + "|",
    ])
    for row in table_rows:
        md_lines.append("| " + " | ".join(row) + " |")
    md_lines.append("")
    return md_lines