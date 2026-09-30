from typing import Literal

from pydantic import BaseModel, Field


GoalType = Literal[
    "weight loss",
    "muscle gain",
    "general wellness",
    "flexibility",
]

IntensityType = Literal[
    "low",
    "medium",
    "high",
]


class UserInput(BaseModel):
    user_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=13, le=100)
    weight: float = Field(..., gt=0)
    goal: GoalType
    intensity: IntensityType


class FeedbackRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    feedback: str = Field(..., min_length=1)


class PlanResponse(BaseModel):
    user_id: str
    name: str
    plan: str
    nutrition_tip: str


class FeedbackResponse(BaseModel):
    user_id: str
    updated_plan: str
    nutrition_tip: str