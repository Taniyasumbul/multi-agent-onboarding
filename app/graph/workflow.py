from __future__ import annotations

from datetime import datetime
from typing import List, TypedDict

from langgraph.graph import END, StateGraph

from app.agents.recommendation_agent import generate_recommendations
from app.agents.status_agent import analyze_status
from app.agents.task_agent import extract_tasks
from app.schemas import Recommendation, Task, TaskStatus


class WorkflowState(TypedDict, total=False):
    onboarding_plan: str
    tasks: List[Task]
    statuses: List[TaskStatus]
    recommendations: List[Recommendation]
    logs: List[str]


def task_node(state: WorkflowState) -> WorkflowState:
    tasks = extract_tasks(state["onboarding_plan"])
    if not tasks:
        raise ValueError("Task extraction produced no tasks")

    logs = state.get("logs", [])
    logs.append(f"{datetime.utcnow().isoformat()} - Extracted {len(tasks)} tasks")

    state["tasks"] = tasks
    state["logs"] = logs
    return state


def status_node(state: WorkflowState) -> WorkflowState:
    statuses = analyze_status(state["tasks"])

    logs = state.get("logs", [])
    logs.append(f"{datetime.utcnow().isoformat()} - Analyzed {len(statuses)} tasks")

    state["statuses"] = statuses
    state["logs"] = logs
    return state


def recommendation_node(state: WorkflowState) -> WorkflowState:
    recs = generate_recommendations(state["statuses"])

    logs = state.get("logs", [])
    logs.append(f"{datetime.utcnow().isoformat()} - Generated {len(recs)} recommendations")

    state["recommendations"] = recs
    state["logs"] = logs
    return state


def build_graph():
    """
    Build and return the compiled LangGraph workflow.
    """
    graph = StateGraph(WorkflowState)

    graph.add_node("tasks", task_node)
    graph.add_node("status", status_node)
    graph.add_node("recommendations", recommendation_node)

    graph.set_entry_point("tasks")
    graph.add_edge("tasks", "status")
    graph.add_edge("status", "recommendations")
    graph.add_edge("recommendations", END)

    return graph.compile()
