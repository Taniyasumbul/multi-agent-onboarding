Multi-Agent Onboarding Workflow (FastAPI + LangGraph + PostgreSQL)

This project implements an AI-powered multi-agent workflow to analyze, break down, and optimize employee onboarding plans. It uses:

LangGraph for agent orchestration

FastAPI for the API service

Neon PostgreSQL for persistence

Modular agents (task extraction, task status analysis, recommendations)

The system converts a raw onboarding plan text into structured tasks, status insights, and actionable recommendations, while saving all results into a cloud database.


🚀 Features

Multi-agent reasoning workflow using LangGraph

Task extraction from free-text onboarding plans

Task status predictions (ok, at_risk, missing_deadline, etc.)

Recommendations generator
Complete run tracking (logs, timestamps)
Full relational database storage (runs, tasks, status, recommendations)
API endpoints using FastAPI
Ready for deployment (Render/)

#Agents:
Task Agent — extracts tasks
Status Agent — analyzes task risk
Recommendation Agent — makes improvement suggestions

Database Tables
runs
tasks
status_analysis
recommendations

📝 Brief Description of Approach
The workflow uses multi-agent reasoning where each agent focuses on a specific task:

Task Agent extracts tasks

Status Agent classifies task risk

Recommendation Agent improves the onboarding plan

LangGraph ensures a deterministic state machine workflow where each agent updates a shared state.
All execution results are stored in NeonDB for auditability.




