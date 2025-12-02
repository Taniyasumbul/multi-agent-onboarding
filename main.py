from fastapi import FastAPI
from app.api.routes import router as api_router
from app.db.database import Base, engine
from app.db import models  # IMPORTANT: models import karna hi hoga

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

# Run table creation when file executed directly
if __name__ == "__main__":
    init_db()

app = FastAPI(title="Onboarding Multi-Agent Workflow")

app.include_router(api_router)
