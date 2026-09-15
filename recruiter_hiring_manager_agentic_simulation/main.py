import asyncio

from app.pipeline import persist_simulation_outputs, run_full_simulation


def print_section(title: str, value: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    print(value)


async def main() -> None:
    results = await run_full_simulation()
    persist_simulation_outputs(results)

    print_section("AVAILABLE JOB CATEGORIES", results["job_titles"])
    print_section("HIRING MANAGER REQUEST", results["job_category"])
    print_section("RECRUITER RESPONSE", results["recruiter_response"])
    print("\n" + "=" * 80)
    print("All outputs are available in the output folder.")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
