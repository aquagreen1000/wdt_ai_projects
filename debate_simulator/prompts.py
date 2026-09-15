"""Prompt construction for debate turns and peer evaluation."""

from .config import WORD_LIMIT


def build_prompt(topic, debater_name, transcript_so_far):
    if transcript_so_far.strip() == "":
        history_section = "No arguments have been made yet. You are speaking first."
    else:
        history_section = (
            "Here is the full debate transcript so far:\n\n"
            f"{transcript_so_far}"
        )

    return f"""You are {debater_name}, a participant in a live debate on the topic:

"{topic}"

You may freely choose and argue any position on this topic (for, against, or a nuanced
stance), based on what strengthens your case given the discussion so far.

{history_section}

Instructions for your turn:
1. If prior arguments exist, provide a concise rebuttal addressing points made so far
   by the other debaters.
2. Then present your own argument or supporting points on the topic.
3. Do NOT invent, fabricate, or make up facts, statistics, studies, or sources. Only use
   reasoning, widely known general knowledge, or points already raised in the debate.
   If you are unsure whether something is factually accurate, do not state it as fact.
4. If you genuinely do not have a strong argument or rebuttal to contribute this turn,
   you may skip by responding with EXACTLY this sentence and nothing else:
   "I don't have any arguments and pass my turn"
5. Your ENTIRE response must be a maximum of {WORD_LIMIT} words. Stay within this limit.
6. Do not include stage directions, meta-commentary, or restate these instructions.
7. Speak in your own voice as {debater_name}.
8. Present arguments as bullets, and avoid long sentences or paragraphs. Use clear,
   concise language.

Now provide your turn:"""


def build_evaluation_prompt(topic, judge_name, other_names, full_transcript):
    others_list = ", ".join(other_names)
    return f"""The debate on the topic "{topic}" has now concluded. Here is the full transcript:

{full_transcript}

You are {judge_name}. You will now act as an impartial judge and evaluate the OTHER
debaters (not yourself): {others_list}.

For each of them, rate the strength of their arguments throughout the debate on a scale
of 1 (worst) to 10 (best), based on logical soundness, relevance, use of rebuttals, and
clarity. Do not favor a debater simply because you agree with their position.

Respond ONLY in the following exact format, with one line per debater you are rating,
and nothing else (no explanations, no extra text):

DebaterName: score

For example:
Debater X: 7
Debater Y: 4

Now provide your ratings for: {others_list}"""