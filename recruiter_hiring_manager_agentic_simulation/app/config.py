from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

BASE_DIR = Path(__file__).resolve().parent.parent
PARENT_DIR = BASE_DIR.parent

for env_path in [BASE_DIR / ".env", PARENT_DIR / ".env", BASE_DIR / ".env.local", PARENT_DIR / ".env.local"]:
    if env_path.exists():
        load_dotenv(env_path, override=True)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
USE_EMAIL = bool(EMAIL_ADDRESS and EMAIL_SMTP_SERVER and EMAIL_APP_PASSWORD)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "google/gemma-4-26b-a4b-it")

if EMAIL_ADDRESS:
    print("Email address is set to:", EMAIL_ADDRESS)
else:
    print("Email address is not set")

if EMAIL_SMTP_SERVER:
    print("SMTP server is set to:", EMAIL_SMTP_SERVER)
else:
    print("SMTP server is not set")

if EMAIL_APP_PASSWORD:
    print("App password is set")
else:
    print("App password is not set")

if USE_EMAIL:
    print("Email is set up and we will try using it")
else:
    print("Email is not set up; we will write local test output instead")

if OPENROUTER_API_KEY:
    print(f"OpenRouter API Key exists and begins {OPENROUTER_API_KEY[:6]}")
else:
    print("OpenRouter API Key not set (and this is optional for local testing)")


def get_openrouter_client() -> AsyncOpenAI:
    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Add it to your environment or .env file."
        )
    return AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )


def get_model():
    return OpenAIChatCompletionsModel(
        model=MODEL_NAME,
        openai_client=get_openrouter_client(),
    )
