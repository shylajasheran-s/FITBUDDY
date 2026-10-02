from sqlalchemy.orm import Session

from ..models import User, WorkoutPlan
from ..schemas import UserInput, FeedbackRequest
from .gemini_service import build_gemini_service


gemini_service = build_gemini_service()


def user_to_dict(user):
    return {
        "id": user.id,
        "user_id": user.user_id,
        "name": user.name,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
    }


def generate_plan_for_user(
    db: Session,
    user_input: UserInput
):
    user = (
        db.query(User)
        .filter(User.user_id == user_input.user_id)
        .first()
    )

    if user is None:
        user = User(
            user_id=user_input.user_id,
            name=user_input.name,
            age=user_input.age,
            weight=user_input.weight,
            goal=user_input.goal,
            intensity=user_input.intensity,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    else:
        user.name = user_input.name
        user.age = user_input.age
        user.weight = user_input.weight
        user.goal = user_input.goal
        user.intensity = user_input.intensity

        db.commit()
        db.refresh(user)

    workout = gemini_service.generate_workout(
        name=user.name,
        age=user.age,
        weight=user.weight,
        goal=user.goal,
        intensity=user.intensity,
    )

    nutrition_tip = gemini_service.generate_tip(
        goal=user.goal,
        weight=user.weight,
    )

    plan = WorkoutPlan(
        user_id=user.id,
        original_plan=workout,
        nutrition_tip=nutrition_tip,
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return {
        "user": user_to_dict(user),
        "plan": workout,
        "nutrition_tip": nutrition_tip,
    }


def update_plan_with_feedback(
    db: Session,
    feedback_request: FeedbackRequest
):
    user = (
        db.query(User)
        .filter(User.user_id == feedback_request.user_id)
        .first()
    )

    if user is None:
        raise ValueError("User not found.")

    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user.id)
        .order_by(WorkoutPlan.created_at.desc())
        .first()
    )

    if plan is None:
        raise ValueError("No workout plan found.")

    current_plan = (
        plan.updated_plan
        if plan.updated_plan
        else plan.original_plan
    )

    updated_plan = gemini_service.update_workout(
        original_plan=current_plan,
        feedback=feedback_request.feedback,
        goal=user.goal,
        intensity=user.intensity,
    )

    plan.updated_plan = updated_plan
    plan.last_feedback = feedback_request.feedback

    db.commit()
    db.refresh(plan)

    return {
        "user": user_to_dict(user),
        "plan": updated_plan,
        "nutrition_tip": plan.nutrition_tip,
    }