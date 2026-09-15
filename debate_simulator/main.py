"""Command-line entry point for the debate simulator."""

if __package__:
    from .debate import run_debate
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from debate_simulator.debate import run_debate

DEFAULT_TOPIC = "Which is the best FIFA 2026 team?"


def main():
    topic = input("Enter the debate topic: ").strip()
    if not topic:
        topic = DEFAULT_TOPIC
        print(f"No topic entered. Using default topic: {topic}")
    run_debate(topic)


if __name__ == "__main__":
    main()