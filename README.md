#  Multi-Agent Onboarding Workflow System  
**AI-powered workflow engine for analyzing onboarding plans using Task Extraction, Status Prediction, and Recommendation Agents.**  
Built with **FastAPI**, **LangGraph**, **Neon PostgreSQL**, and  **Gemini API integration**.

---

##  Overview  
This project is an **LLM-powered multi-agent onboarding workflow system**.  
It takes an onboarding plan as input and automatically:

1️⃣ Extracts tasks  
2️⃣ Analyzes the status of each task  
3️⃣ Generates actionable recommendations  
4️⃣ Saves everything into a Neon PostgreSQL database  
5️⃣ Returns a structured response with tasks, status, recommendations & logs  

---

##  Architecture

                        ┌───────────────────────────────┐
                        │          Client / UI           │
                        │ (Swagger, Postman, Frontend)   │
                        └───────────────┬───────────────┘
                                        │ HTTP Request
                                        ▼
                            ┌──────────────────────┐
                            │      FastAPI API     │
                            │  /run_onboarding...  │
                            └───────┬──────────────┘
                                    │
                                    ▼
                      ┌─────────────────────────────┐
                      │     LangGraph Workflow       │
                      │  (State Machine + Agents)    │
                      └───────────┬──────────────────┘
                                  │
                ┌─────────────────┼──────────────────┐
                │                 │                  │
                ▼                 ▼                  ▼
        ┌─────────────┐  ┌─────────────────┐  ┌────────────────────┐
        │ Task Agent   │  │ Status Agent    │ │ RecommendationAgent│
        │ Extracts     │  │ Predicts status │ │ Creates suggestions│
        │ structured   │  │ (risk/ok/...)   │ │ from task insights │
        │ tasks        │  └─────────────────┘ └────────────────────┘
        └─────────────┘
                │
                ▼
     ┌────────────────────┐
     │   Aggregated State │
     │ (tasks + statuses +│
     │ recommendations)    │
     └───────────┬────────┘
                 │
                 ▼
       ┌────────────────────────┐
       │ Neon PostgreSQL Cloud   │
       │   - runs               │
       │   - tasks              │
       │   - status_analysis    │
       │   - recommendations    │
       └────────────────────────┘
