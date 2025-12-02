from __future__ import annotations

from typing import List

from app.schemas import TaskStatus, Recommendation


def generate_recommendations(statuses: List[TaskStatus]) -> List[Recommendation]:
    recs: List[Recommendation] = []

    for s in statuses:
        if s.status == "delayed":
            recs.append(
                Recommendation(
                    message=(
                        f"Task '{s.task_title}' is delayed. "
                        "Escalate to the owner and agree on a new deadline."
                    ),
                    severity="high",
                )
            )
        elif s.status == "at_risk":
            recs.append(
                Recommendation(
                    message=(
                        f"Task '{s.task_title}' is at risk due to missing or unclear "
                        "timeline. Clarify scope and set a due date."
                    ),
                    severity="medium",
                )
            )

    if not recs:
        recs.append(
            Recommendation(
                message="All tasks appear on track. No escalation needed.",
                severity="low",
            )
        )

    return recs
