# CrewAI Agent Reference

This document is the general CrewAI reference for this project. It covers the framework concepts and coding patterns used when defining agents and crews in CrewAI.

## Core concepts

- Agent: a role-based autonomous worker with a goal, backstory, tools, and an LLM.
- Task: a unit of work assigned to an agent or a group of agents.
- Crew: a collection of agents and tasks orchestrated together.
- Process: execution mode, usually sequential or hierarchical.

## Recommended CrewAI pattern

Use the CrewBase decorator and YAML-based configuration for agents and tasks.

```python
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

@CrewBase
class ExampleCrew:
    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
```

## Agent config

Agents are usually defined in YAML:

```yaml
engineering_lead:
  role: >
    Engineering Lead
  goal: >
    Design the solution and assign work.
  backstory: >
    You're a seasoned engineering lead.
  llm: openai/gpt-4.1-mini
```

Task config is also YAML-based:

```yaml
design_task:
  description: >
    Create a detailed technical design.
  expected_output: >
    A markdown design document.
  agent: engineering_lead
```

## Important rules

- Add `# type: ignore[index]` when accessing config dictionaries.
- Agent method names must match YAML keys exactly.
- Tools belong on agents unless a task-specific tool override is needed.
- Namespacing and file locations should match the project structure.

## LLM usage

Prefer CrewAI-native LLM usage rather than raw OpenAI clients.

```python
from crewai import LLM

agent = Agent(llm="openai/gpt-4o")
# or
agent = Agent(llm=LLM(model="openai/gpt-4o"))
```

## Execution patterns

```python
result = crew.kickoff(inputs={"requirements": "..."})
```

Common execution styles:

- crew.kickoff(inputs=...): run a crew synchronously
- crew.akickoff(inputs=...): async run
- crew.kickoff_for_each(inputs=[...]): batch execution
- flow.kickoff(): run a flow-based orchestration

## Tools and sandbox integration

CrewAI tools can be simple Python functions decorated with `@tool`, or custom classes that extend BaseTool. In this repository, the agents use sandbox tools to read/write files and run Python scripts in a shared workspace.

```python
from crewai.tools import tool

@tool("List Sandbox Files")
def list_sandbox_files() -> str:
    return "file1.py\nfile2.py"
```

## When to use sequential vs hierarchical process

- Sequential: best for staged engineering workflows where each step depends on the previous one.
- Hierarchical: best when a manager delegates tasks dynamically among agents.

This project uses sequential execution because the work must follow a strict order: requirements -> design -> implementation -> frontend -> validation -> testing.

## Summary

CrewAI is a framework for coordinating multi-agent software work. The key idea is to define specialized roles, assign tasks, and let the crew operate through a controlled workflow. For this repository, that workflow is a sequential engineering process that builds and tests a trading simulation app in a sandbox.
