"""Bounded LangGraph review loop; secrets are supplied only through environment variables."""

from __future__ import annotations

import os
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph


class WorkState(TypedDict, total=False):
    task: str
    plan: str
    implementation_brief: str
    review: str
    cycles: int
    approved: bool


def _model() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "deepseek-chat"),
        base_url=os.getenv("OPENAI_API_BASE", "http://127.0.0.1:14000/v1"),
        api_key=os.environ["OPENAI_API_KEY"],
        temperature=0,
    )


def build_graph(max_cycles: int | None = None):
    limit = max_cycles or int(os.getenv("MAX_REVIEW_CYCLES", "3"))

    def plan(state: WorkState) -> WorkState:
        response = _model().invoke(
            "Act as a staff software architect. Create a concise, testable implementation plan. "
            "Do not claim to have modified files.\nTASK:\n" + state["task"]
        )
        return {"plan": str(response.content), "cycles": 0}

    def implement_brief(state: WorkState) -> WorkState:
        response = _model().invoke(
            "Prepare an execution brief for OpenHands. Include acceptance criteria, tests, "
            "security constraints, and rollback notes. Do not claim execution.\n"
            f"PLAN:\n{state['plan']}\nTASK:\n{state['task']}\n"
            f"PREVIOUS REVIEW:\n{state.get('review', 'none')}"
        )
        return {"implementation_brief": str(response.content)}

    def review(state: WorkState) -> WorkState:
        response = _model().invoke(
            "Review this proposed execution brief for completeness, testability, security, "
            "and reversibility. Return APPROVED only if all criteria are explicit; otherwise "
            "return CHANGES REQUIRED and concise findings.\n" + state["implementation_brief"]
        )
        verdict = str(response.content)
        cycles = state.get("cycles", 0) + 1
        return {
            "review": verdict,
            "cycles": cycles,
            "approved": verdict.strip().upper().startswith("APPROVED"),
        }

    def route(state: WorkState) -> str:
        if state.get("approved") or state.get("cycles", 0) >= limit:
            return "done"
        return "revise"

    graph = StateGraph(WorkState)
    graph.add_node("plan", plan)
    graph.add_node("implement_brief", implement_brief)
    graph.add_node("review", review)
    graph.add_edge(START, "plan")
    graph.add_edge("plan", "implement_brief")
    graph.add_edge("implement_brief", "review")
    graph.add_conditional_edges("review", route, {"revise": "implement_brief", "done": END})
    return graph.compile()


def run_task(task: str) -> WorkState:
    if not task.strip():
        raise ValueError("task must not be empty")
    return build_graph().invoke({"task": task})
