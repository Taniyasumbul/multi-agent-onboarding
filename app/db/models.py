from datetime import datetime, date

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String, unique=True, index=True)
    input_text = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    tasks = relationship("Task", back_populates="run", cascade="all, delete-orphan")
    statuses = relationship(
        "StatusAnalysis", back_populates="run", cascade="all, delete-orphan"
    )
    recommendations = relationship(
        "Recommendation", back_populates="run", cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    owner = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    run = relationship("Run", back_populates="tasks")
    statuses = relationship(
        "StatusAnalysis", back_populates="task", cascade="all, delete-orphan"
    )


class StatusAnalysis(Base):
    __tablename__ = "status_analysis"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    status = Column(String, nullable=False)
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    run = relationship("Run", back_populates="statuses")
    task = relationship("Task", back_populates="statuses")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"))
    message = Column(Text, nullable=False)
    severity = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    run = relationship("Run", back_populates="recommendations")
