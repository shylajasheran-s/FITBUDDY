from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db
from .models import User, WorkoutPlan
from .schemas import FeedbackRequest, UserInput
from .services.plan_service import (
    generate_plan_for_user,
    update_plan_with_feedback,
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

settings = get_settings()


# -------------------------
# Home Page
# -------------------------
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
        },
    )


# -------------------------
# Generate Workout
# -------------------------
@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    user_input = UserInput(
        user_id=user_id,
        name=name,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
    )

    try:
        result = generate_plan_for_user(db, user_input)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "user": result["user"],
                "plan": result["plan"],
                "nutrition_tip": result["nutrition_tip"],
            },
        )

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": str(exc),
            },
            status_code=500,
        )


# -------------------------
# Feedback Page
# -------------------------
@router.get("/feedback/{user_id}", response_class=HTMLResponse)
def feedback_page(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return templates.TemplateResponse(
        request=request,
        name="feedback.html",
        context={
            "request": request,
            "user": user,
        },
    )


# -------------------------
# Submit Feedback
# -------------------------
@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    feedback_request = FeedbackRequest(
        user_id=user_id,
        feedback=feedback,
    )

    try:
        result = update_plan_with_feedback(
            db,
            feedback_request,
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "user": result["user"],
                "plan": result["plan"],
                "nutrition_tip": result["nutrition_tip"],
                "feedback_updated": True,
            },
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# -------------------------
# Admin - View All Users
# -------------------------
@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(
    request: Request,
    password: str = "",
    db: Session = Depends(get_db),
):
    if password != settings.admin_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin password",
        )

    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users,
        },
    )


# -------------------------
# API - Users
# -------------------------
@router.get("/api/users")
def api_users(
    db: Session = Depends(get_db),
):
    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )

    return [
        {
            "id": user.id,
            "user_id": user.user_id,
            "name": user.name,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
        }
        for user in users
    ]


# -------------------------
# API - Generate Workout
# -------------------------
@router.post("/api/generate-workout")
def api_generate_workout(
    user_input: UserInput,
    db: Session = Depends(get_db),
):
    try:
        result = generate_plan_for_user(
            db,
            user_input,
        )

        return {
            "user": result["user"],
            "plan": result["plan"],
            "nutrition_tip": result["nutrition_tip"],
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# -------------------------
# API - Feedback
# -------------------------
@router.post("/api/feedback")
def api_feedback(
    feedback_request: FeedbackRequest,
    db: Session = Depends(get_db),
):
    try:
        result = update_plan_with_feedback(
            db,
            feedback_request,
        )

        return {
            "user": result["user"],
            "plan": result["plan"],
            "nutrition_tip": result["nutrition_tip"],
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# -------------------------
# Health Check
# -------------------------
@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": settings.app_name,
    }