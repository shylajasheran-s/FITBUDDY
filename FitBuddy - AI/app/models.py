from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)

    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)

    goal = Column(String(100), nullable=False)
    intensity = Column(String(50), nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    workout_plans = relationship(
        "WorkoutPlan",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    original_plan = Column(Text, nullable=False)

    updated_plan = Column(
        Text,
        nullable=True,
    )

    nutrition_tip = Column(
        Text,
        nullable=True,
    )

    last_feedback = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="workout_plans",
    )