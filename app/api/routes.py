from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.crud import save_run
from app.db.database import get_db
from app.graph.workflow import build_graph
from app.schemas import Recommendation, RunResult, Task, TaskStatus

router = APIRouter()


class OnboardingRequest(BaseModel):
    onboarding_plan: str


_graph = build_graph()


@router.post("/run_onboarding_agents", response_model=RunResult)
def run_onboarding_agents(
    req: OnboardingRequest,
    db: Session = Depends(get_db),
):
    if not req.onboarding_plan.strip():
        raise HTTPException(status_code=400, detail="onboarding_plan cannot be empty")

    started_at = datetime.utcnow()

    # Run LangGraph workflow
    state = {"onboarding_plan": req.onboarding_plan}
    try:
        result_state = _graph.invoke(state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow failed: {e}")

    # Convert state back to Pydantic models
    tasks = [Task(**t) if not isinstance(t, Task) else t for t in result_state["tasks"]]
    statuses = [
        TaskStatus(**s) if not isinstance(s, TaskStatus) else s
        for s in result_state["statuses"]
    ]
    recs = [
        Recommendation(**r) if not isinstance(r, Recommendation) else r
        for r in result_state["recommendations"]
    ]
    logs = result_state.get("logs", [])

    # Save to DB transactionally
    try:
        run_id = save_run(db, req.onboarding_plan, tasks, statuses, recs)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finished_at = datetime.utcnow()

    return RunResult(
        run_id=run_id,
        started_at=started_at,
        finished_at=finished_at,
        tasks=tasks,
        statuses=statuses,
        recommendations=recs,
        logs=logs,
    )


@router.get("/health")
def health_check():
    return {"status": "ok"}
