# Engineering Team

This project is a CrewAI-based multi-agent engineering workflow that turns a plain software specification into a working implementation in a sandboxed environment. The system acts like a small internal software team: an engineering lead designs the solution, engineers implement the backend and UI, and a QA engineer writes and runs tests until the result passes.

The project is designed around a trading simulation/account management system. It does not simply answer questions with an LLM — it orchestrates agents to write real code, execute it, validate it, and keep iterating on the result.

## What the project does

The crew is given a set of high-level requirements for a trading app and then performs the following workflow:

1. Design phase
   - The engineering lead reviews the requirements.
   - It produces a technical design with modules, classes, and method signatures.
   - The design is saved to the sandbox as a design document.

2. Backend implementation
   - The backend engineer writes Python code to satisfy the design.
   - The implementation includes account management, deposits, withdrawals, stock buys and sells, portfolio calculations, holdings, and transaction history.
   - The code is written into a sandbox project and tested using the standard library.

3. Frontend implementation
   - The frontend engineer builds a Gradio app that demonstrates the backend behavior.
   - The UI allows users to create accounts, deposit funds, withdraw funds, buy/sell shares, inspect holdings, and review transactions.
   - A validation script confirms the frontend module can construct successfully without launching the app.

4. Test phase
   - The test engineer writes unit tests using the built-in unittest framework.
   - Tests confirm the backend logic works and the frontend object can be initialized.
   - Any bugs are fixed iteratively until the suite passes.

## High-level architecture

The project is organized as a CrewAI crew with specialized agents defined in the source package:

- [src/engineering_team/crew.py](src/engineering_team/crew.py) defines the agent and task orchestration.
- [src/engineering_team/main.py](src/engineering_team/main.py) is the entry point for running the crew locally.
- [src/engineering_team/config/agents.yaml](src/engineering_team/config/agents.yaml) defines the engineering_lead, backend_engineer, frontend_engineer, and test_engineer roles.
- [src/engineering_team/config/tasks.yaml](src/engineering_team/config/tasks.yaml) defines the design, implementation, frontend, and test tasks.
- [src/engineering_team/tools/sandbox_tools.py](src/engineering_team/tools/sandbox_tools.py) gives the agents tools to list, read, write, and execute files in the sandbox project.
- [src/engineering_team/patch.py](src/engineering_team/patch.py) includes a CrewAI compatibility patch for MCP tool name handling.

## Sandbox workflow

The app creates and manages a working project under the [sandbox](sandbox) directory. That sandbox acts as a disposable workspace where the agents build code and run tests.

The sandbox tools support:

- Listing files in the generated project
- Reading file contents
- Writing new implementation files
- Executing Python scripts in a uv-managed environment
- Running tests in a containerized or local execution environment

This lets the AI team work like a software development pipeline instead of a single prompt-only assistant.

## Functional scope

The generated system is meant to model a trading simulation platform with these core behaviors:

- Create user accounts
- Deposit funds
- Withdraw funds while enforcing balance rules
- Record buy and sell actions with quantity data
- Calculate portfolio value
- Track profit and loss from the initial deposit
- Report current holdings
- Show transaction history
- Prevent invalid operations such as overdraft withdrawals, unaffordable purchases, and selling stock the user does not own

The requirements also specify that every function gets unit tests using Python's unittest module and that the app can be demonstrated through a Gradio interface.

## Project entry points

The package exposes several local execution utilities from [pyproject.toml](pyproject.toml):

- engineering_team / run_crew: start the crew
- train: train the crew over iterations
- replay: replay a task from an earlier run
- test: run crew evaluation
- run_with_trigger: start the workflow from a JSON trigger payload

## How to run it

From the project root:

```bash
uv sync
uv run engineering_team
```

Or use the script entry points directly:

```bash
uv run run_crew
```

This initializes the crew and kicks off the full engineering workflow.

## Dependencies

This project depends on:

- Python 3.10 to 3.13
- CrewAI
- Gradio in the sandbox for the frontend work
- Docker/UV-based execution for sandbox code runs

## Notes

The important idea behind this repository is not a finished app by itself, but an autonomous software generation loop: the AI agents collaborate to design, implement, validate, and refine an application in a real sandboxed workspace. The result is a practical example of an LLM-based engineering team being used to build and test a small software system end-to-end.
