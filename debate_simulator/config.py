"""Configuration for the local Ollama debate simulator."""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

DEBATERS = [
    {"name": "Debater Aria", "model": "gemma2:2b"},
    {"name": "Debater Ben", "model": "qwen3:4b"},
    {"name": "Debater Cyrus", "model": "llama3.2:latest"},
]

TURNS_PER_DEBATER = 4
WORD_LIMIT = 250
TRANSCRIPT_FILE = "debate_transcript.md"