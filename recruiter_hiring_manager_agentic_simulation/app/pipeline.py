from __future__ import annotations

from typing import Any

from agents import Runner

from .agents import build_agents, get_default_job_titles
from .notifications import send_message, write_html_output


async def generate_cv_bank(job_titles: list[str] | None = None, agent: Any | None = None) -> str:
    titles = job_titles or get_default_job_titles()
    cv_agent = agent or build_agents()["cv_generator_agent"]
    cv_bank = await Runner.run(
        cv_agent,
        input="Generate CVs for the following job titles: " + ", ".join(titles),
    )
    return cv_bank.final_output


async def generate_job_category(job_titles: list[str] | None = None, agent: Any | None = None) -> str:
    titles = job_titles or get_default_job_titles()
    hiring_agent = agent or build_agents()["hiring_manager_agent"]
    query = await Runner.run(
        hiring_agent,
        input="Please provide a job description phrase from " + ", ".join(titles),
    )
    return query.final_output


async def generate_recruiter_response(job_category: str, cv_bank: str, agent: Any | None = None) -> str:
    recruiter_agent = agent or build_agents()["recruiter_agent"]
    response = await Runner.run(
        recruiter_agent,
        input=f"{job_category} Here are the CVs: {cv_bank}",
    )
    return response.final_output


async def run_full_simulation(job_titles: list[str] | None = None) -> dict[str, str]:
    titles = job_titles or get_default_job_titles()
    agents = build_agents()

    cv_bank = await generate_cv_bank(titles, agents["cv_generator_agent"])
    job_category = await generate_job_category(titles, agents["hiring_manager_agent"])
    recruiter_response = await generate_recruiter_response(job_category, cv_bank, agents["recruiter_agent"])

    return {
        "job_titles": ", ".join(titles),
        "cv_bank": cv_bank,
        "job_category": job_category,
        "recruiter_response": recruiter_response,
    }


def persist_simulation_outputs(results: dict[str, str]) -> None:
    write_html_output("simulated_CVs.html", results["cv_bank"])
    write_html_output("recruiter_recommendations.html", results["recruiter_response"])
    send_message(
        "Recruiter Recommendations",
        results["recruiter_response"],
        f"<html><body>{results['recruiter_response']}</body></html>",
    )
