"""LLM calls used by the debate simulator."""

from .config import client


def call_ollama(model, prompt):
    """Return a model response, or a readable error for the transcript."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as error:
        return f"[ERROR: Could not get response from model '{model}': {error}]"