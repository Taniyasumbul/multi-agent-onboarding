from __future__ import annotations

import json
import os
import re
from datetime import datetime
from typing import List

import google.generativeai as genai

from app.config import settings
from app.schemas import Task


def _init_gemini_model():
    api_key = settings.gemini_api_key
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


_gemini_model = _init_gemini_model()


def _call_gemini_for_tasks(onboarding_plan: str) -> List[Task]:
    """
    Ask Gemini to extract tasks as JSON.
    """
    if _gemini_model is None:
        raise RuntimeError("Gemini API key not configured")

    prompt = f"""
You are an assistant that extracts onboarding tasks.

Return ONLY valid JSON (no markdown) as a list of objects with:
- title (string)
- description (string)
- owner (string or null)
- due_date (ISO date string YYYY-MM-DD or null)

Onboarding plan:
\"\"\"{onboarding_plan}\"\"\""""

    response = _gemini_model.generate_content(prompt)
    text = response.text.strip()

    # Sometimes Gemini wraps JSON in ```json ..``` – strip that.
    text = re.sub(r"```json|```", "", text).strip()

    data = json.loads(text)
    return [Task(**t) for t in data]


def _simple_fallback_tasks(onboarding_plan: str) -> List[Task]:
    """
    Very simple rule-based extractor used if Gemini not available.
    It treats numbered lines like '1. Kickoff Call' as tasks.
    """
    lines = onboarding_plan.splitlines()
    tasks: List[Task] = []
    current_title = None
    buffer: list[str] = []

    for line in lines:
        if re.match(r"^\s*\d+\.\s+", line):
            # flush previous
            if current_title:
                tasks.append(
                    Task(
                        title=current_title,
                        description="\n".join(buffer).strip() or current_title,
                        owner=None,
                        due_date=None,
                    )
                )
                buffer = []
            current_title = re.sub(r"^\s*\d+\.\s+", "", line).strip()
        else:
            buffer.append(line)

    if current_title:
        tasks.append(
            Task(
                title=current_title,
                description="\n".join(buffer).strip() or current_title,
                owner=None,
                due_date=None,
            )
        )

    # if nothing found, create a single generic task
    if not tasks:
        tasks.append(
            Task(
                title="Review onboarding plan",
                description=onboarding_plan[:500],
                owner=None,
                due_date=None,
            )
        )

    return tasks


def extract_tasks(onboarding_plan: str) -> List[Task]:
    """
    Main entry: try Gemini, if it fails, use rule-based fallback.
    """
    try:
        if _gemini_model is not None:
            return _call_gemini_for_tasks(onboarding_plan)
    except Exception as e:
        print(f"[TaskAgent] Gemini failed, using fallback. Error: {e}")

    return _simple_fallback_tasks(onboarding_plan)
