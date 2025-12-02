from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    title: str
    description: str
    owner: Optional[str] = None
    due_date: Optional[date] = None


class TaskStatus(BaseModel):
    task_title: str
    status: str = Field(description="on_track | delayed | at_risk")
    explanation: str


class Recommendation(BaseModel):
    message: str
    severity: str = Field(description="low | medium | high")


class RunResult(BaseModel):
    run_id: str
    started_at: datetime
    finished_at: datetime
    tasks: List[Task]
    statuses: List[TaskStatus]
    recommendations: List[Recommendation]
    logs: List[str] = []
