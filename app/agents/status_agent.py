from __future__ import annotations

from datetime import date
from typing import List

from app.schemas import Task, TaskStatus


def analyze_status(tasks: List[Task], today: date | None = None) -> List[TaskStatus]:
    """
    Simple status logic:
    - if no due_date -> at_risk
    - if due_date < today -> delayed
    - else on_track
    """
    if today is None:
        today = date.today()

    result: List[TaskStatus] = []
    for t in tasks:
        if t.due_date is None:
            status = "at_risk"
            explanation = "No due date specified."
        elif t.due_date < today:
            status = "delayed"
            explanation = f"Due date {t.due_date} has already passed."
        else:
            status = "on_track"
            explanation = f"Due date {t.due_date} is in the future."

        result.append(
            TaskStatus(task_title=t.title, status=status, explanation=explanation)
        )

    return result
