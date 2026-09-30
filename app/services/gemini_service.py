from ..config import get_settings


class GeminiService:

    def __init__(self):
        self.settings = get_settings()

    def generate_workout(
        self,
        name,
        age,
        weight,
        goal,
        intensity
    ):

        if self.settings.ai_demo_mode:
            return f"""
FITBUDDY 7-DAY WORKOUT PLAN

User: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

DAY 1
Warm-up:
5-10 minutes walking and stretching.

Main Workout:
- Squats - 3 x 12
- Push-ups - 3 x 10
- Lunges - 3 x 10
- Plank - 3 x 30 seconds

Cool-down:
5 minutes stretching.

DAY 2
Warm-up:
5-10 minutes light cardio.

Main Workout:
- Brisk walking - 20 minutes
- Glute bridges - 3 x 15
- Shoulder raises - 3 x 12
- Bicycle crunches - 3 x 15

Cool-down:
5 minutes stretching.

DAY 3
Active Recovery:
- Walking - 20 minutes
- Light stretching

DAY 4
Warm-up:
5-10 minutes.

Main Workout:
- Squats - 3 x 12
- Push-ups - 3 x 10
- Step-ups - 3 x 12
- Plank - 3 x 30 seconds

Cool-down:
5 minutes stretching.

DAY 5
Cardio:
- Walking or cycling - 25 minutes

Core:
- Crunches - 3 x 15
- Plank - 3 x 30 seconds

DAY 6
Full Body:
- Squats - 3 x 12
- Lunges - 3 x 10
- Push-ups - 3 x 10
- Glute bridges - 3 x 15

DAY 7
Recovery:
- Light walking
- Mobility exercises
- Full-body stretching

Recovery:
Stay hydrated and get enough sleep.
"""

        return "Unable to generate workout."


    def generate_tip(self, goal, weight):

        if self.settings.ai_demo_mode:
            return (
                "Stay hydrated, eat balanced meals with enough "
                "protein and vegetables, and maintain a consistent "
                "sleep schedule."
            )

        return "Nutrition tip unavailable."


    def update_workout(
        self,
        original_plan,
        feedback,
        goal,
        intensity
    ):

        if self.settings.ai_demo_mode:
            return f"""
UPDATED FITBUDDY WORKOUT PLAN

Goal: {goal}
Intensity: {intensity}

User Feedback:
{feedback}

Updated Plan:

1. Adjust workout intensity according to the feedback.
2. Include suitable warm-up exercises.
3. Include appropriate main exercises.
4. Include cool-down and recovery exercises.
5. Maintain proper hydration and rest.

Previous Plan:
{original_plan}
"""

        return "Unable to update workout."


def build_gemini_service():
    return GeminiService()