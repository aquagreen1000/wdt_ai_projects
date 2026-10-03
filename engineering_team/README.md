# Engineering Team

This repository is a small, end-to-end demonstration of agentic software engineering. Instead of just answering a question, the project uses CrewAI agents to design, implement, test, and refine a trading account simulator inside a disposable sandbox.

The result is a working example of a multi-agent development loop: one agent writes the design, another implements the backend, another builds the UI, and a QA agent verifies behavior and fixes issues until the code passes its tests.

## What this project does

The crew is given a specification for a trading simulation and account-management system. It then carries out the following workflow:

1. Design the solution
   - The engineering lead reads the requirements.
   - It drafts a technical design that defines the modules, classes, and expected behaviors.
   - The design is stored in the sandbox as a design document for the rest of the team to use.

2. Implement the backend
   - The backend engineer creates Python logic for managing users, cash balances, stock transactions, holdings, and portfolio values.
   - Supported actions include creating accounts, depositing and withdrawing cash, buying and selling stock, calculating portfolio value, and tracking profit/loss.
   - The implementation is written into a sandbox project so it behaves like a real code workspace rather than a one-off prompt output.

3. Build the demo UI
   - The frontend engineer creates a Gradio interface that lets a user interact with the backend through a browser.
   - The UI includes tabs for account creation, deposits, withdrawals, buys, sells, holdings, portfolio value, and transaction history.
   - A validation step ensures the interface can construct successfully without a full interactive launch.

4. Validate and iterate
   - The test engineer writes Python unittest checks for the backend logic and basic UI construction.
   - The team runs those tests, inspects failures, and corrects the implementation until the suite passes.

This is not just a toy chatbot. It is a real software development pattern in which the agents operate on files, execute code, and improve the result over time.

## Project structure

- [src/engineering_team/crew.py](src/engineering_team/crew.py) defines the CrewAI crew and all four specialized agents.
- [src/engineering_team/main.py](src/engineering_team/main.py) is the local entry point that resets the sandbox and runs the crew.
- [src/engineering_team/config/agents.yaml](src/engineering_team/config/agents.yaml) contains the engineering_lead, backend_engineer, frontend_engineer, and test_engineer definitions.
- [src/engineering_team/config/tasks.yaml](src/engineering_team/config/tasks.yaml) contains the design, code, frontend, and QA tasks.
- [src/engineering_team/tools/sandbox_tools.py](src/engineering_team/tools/sandbox_tools.py) gives the agents tools to list files, read or write code, and run Python in the sandbox.
- [sandbox/account_backend.py](sandbox/account_backend.py) holds the actual trading/account logic used by the generated app.
- [sandbox/app.py](sandbox/app.py) is the Gradio front end that exposes the backend to the user.
- [sandbox/test_backend.py](sandbox/test_backend.py) contains the unittest suite for the account manager.
- [src/engineering_team/patch.py](src/engineering_team/patch.py) patches CrewAI compatibility for MCP tool names.

## Functional behavior of the generated app

The code in the sandbox models a trading simulation platform with these capabilities:

- Create a user account with an initial cash deposit
- Deposit or withdraw cash with validation
- Buy or sell stock by symbol and quantity
- Enforce affordability and ownership checks
- Track holdings for each user
- Calculate total portfolio value and profit/loss from the initial deposit
- Keep a transaction log with timestamps and amounts
- Handle invalid actions such as negative deposits, overdrafts, overbuying, or selling more shares than are owned

The sample stock price lookup uses fixed prices for AAPL, TSLA, and GOOGL and raises an error for unsupported symbols.

## Sandbox workflow

The repository builds a fresh project under the [sandbox](sandbox) folder each time the crew runs. That sandbox acts as a temporary working directory where the agents can write code and run tests without affecting the rest of the repo.

The sandbox tools expose a minimal but useful development loop:

- list files in the generated project
- read a file's content
- write implementation code
- execute a Python file in a uv-based environment
- inspect stdout and stderr from test or validation runs

This is the key idea of the project: AI agents are not only generating ideas, they are operating on files and iterating on working software in a local workspace.

## How to run it

From the project root:

```bash
uv sync
uv run engineering_team
```

You can also invoke the entry points declared in [pyproject.toml](pyproject.toml):

```bash
uv run run_crew
```

The `run` function resets the sandbox, starts the CrewAI workflow, and executes the full design/build/test loop.

## Project commands

The package exposes a few useful local commands:

- `engineering_team` / `run_crew`: run the full crew
- `train`: train the crew with additional iterations
- `replay`: replay a previously executed task
- `test`: run the crew evaluation flow
- `run_with_trigger`: execute the crew from a JSON trigger payload

## Dependencies

This project depends on:

- Python 3.10 to 3.13
- CrewAI
- Gradio for the demo UI in the sandbox
- Docker and uv for running code in the sandbox environment

## Notes

This repository is best understood as a working example of an autonomous engineering team, not as a standalone product app. The important artifact is the system that coordinates agents to create, validate, and refine code in a real sandboxed workflow.

In other words, the app is the demonstration target, but the bigger project goal is to show how AI agents can collaborate on software development tasks end-to-end.
