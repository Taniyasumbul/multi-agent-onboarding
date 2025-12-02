from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db import models
from app.schemas import Task, TaskStatus, Recommendation


def save_run(
    db: Session,
    input_text: str,
    tasks: List[Task],
    statuses: List[TaskStatus],
    recs: List[Recommendation],
) -> str:
    run_uuid = str(uuid4())
    run = models.Run(
        run_id=run_uuid,
        input_text=input_text,
        started_at=datetime.utcnow(),
        finished_at=datetime.utcnow(),
    )
    db.add(run)
    db.flush()  # to get run.id

    # map task title -> row id
    title_to_id: dict[str, int] = {}

    for t in tasks:
        row = models.Task(
            run_id=run.id,
            title=t.title,
            description=t.description,
            owner=t.owner,
            due_date=t.due_date,
        )
        db.add(row)
        db.flush()
        title_to_id[t.title] = row.id

    for s in statuses:
        task_id = title_to_id.get(s.task_title)
        status_row = models.StatusAnalysis(
            run_id=run.id,
            task_id=task_id,
            status=s.status,
            explanation=s.explanation,
        )
        db.add(status_row)

    for r in recs:
        rec_row = models.Recommendation(
            run_id=run.id,
            message=r.message,
            severity=r.severity,
        )
        db.add(rec_row)

    return run_uuid
