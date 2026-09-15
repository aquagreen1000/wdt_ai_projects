from __future__ import annotations

from agents import Agent

from .config import get_model

CV_GENERATION_INSTRUCTION = """
You are a helpful assistant that generates CVs for job applications.
You will receive a list of job titles. For each title, generate between 1-3 CVs in the following format:
first_name, last_name,
education - less than 10 words
work_experience highlighting 2-3 fictitious roles - less than 100 words
skills relevant to the job title - less than 50 words.
The agent should return an array of CVs in JSON format with the following structure:
first_name, last_name, education, work_experience, skills.
"""

RECRUITER_INTRO = """
You will receive a job title phrase from the hiring manager.

You task is to review all the CVs and send the name of one top matching candidate to the hiring manager.

If you do not find a good match, you should send an email to the hiring manager that you did not find a good match.

If the title phrase is not clear, you should send an email to the hiring manager for clarification without reviewing the CVs.

You should not make assumptions about the job title. You should only review the CVs if you have a clear understanding of the job title phrase.
"""

HIRING_MANAGER_INTRO = """
You are a hiring manager in a tech company who is looking for candidates for a position in a large software development group.
You will provide a 2-3 word job description phrase to the recruiter.
Be concise and clear.

Example: "Senior Data Scientist", "scrum master", "frontend developer", "backend engineer", "full stack developer", "machine learning engineer", "data analyst", "product manager", "UX designer", "DevOps engineer", "cloud architect", "cybersecurity specialist", "AI researcher", "mobile app developer", "blockchain developer", "game developer", "embedded systems engineer", "network administrator", "IT support specialist".
"""


def get_default_job_titles() -> list[str]:
    return [
        "Senior Data Scientist",
        "Scrum Master",
        "Frontend Developer",
        "Backend Engineer",
        "Full Stack Developer",
        "Machine Learning Engineer",
        "Data Analyst",
        "Product Manager",
        "UX Designer",
        "DevOps Engineer",
    ]


def build_cv_generator_agent() -> Agent:
    return Agent(
        name="cv_generator_agent",
        instructions=CV_GENERATION_INSTRUCTION,
        model=get_model(),
    )


def build_recruiter_agent() -> Agent:
    recruiter_instructions = RECRUITER_INTRO + "Your email style is professional. You should highlight the candidate name and top 3 matching themes."
    return Agent(
        name="Recruiter_Agent",
        instructions=recruiter_instructions,
        model=get_model(),
    )


def build_hiring_manager_agent() -> Agent:
    hiring_manager_instructions = HIRING_MANAGER_INTRO + "Your email style is professional and concise."
    return Agent(
        name="Hiring_Manager_Agent",
        instructions=hiring_manager_instructions,
        model=get_model(),
    )


def build_agents() -> dict[str, Agent]:
    return {
        "cv_generator_agent": build_cv_generator_agent(),
        "recruiter_agent": build_recruiter_agent(),
        "hiring_manager_agent": build_hiring_manager_agent(),
    }
