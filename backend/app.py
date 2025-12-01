import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.exceptions import ModelProviderError


# -----------------------------------------------------
# 🔑 GOOGLE GEMINI API KEY  (YOUR KEY INCLUDED)
# -----------------------------------------------------
os.environ["GOOGLE_API_KEY"] = "AIzaSyB682-c0i7Pv9sDt0TIHTtqgkKNdc_t25k"

# 🔥 Stable Gemini Model
GEMINI_MODEL_ID = "gemini-2.0-flash-001"


# -----------------------------------------------------
# 🚀 FASTAPI INITIAL SETUP
# -----------------------------------------------------
app = FastAPI()

# Allow any frontend to connect (React, HTML, Flutter, Android)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow ALL origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input Model
class UserInput(BaseModel):
    name: str
    age: int
    weight: float
    height: float
    activity_level: str
    dietary_preference: str
    fitness_goal: str


# -----------------------------------------------------
# 🤖 AGENT DEFINITIONS
# -----------------------------------------------------

dietary_planner = Agent(
    model=Gemini(id=GEMINI_MODEL_ID),
    description="Creates personalized dietary plans.",
    instructions=[
        "Generate breakfast, lunch, dinner, and snacks.",
        "Adjust based on dietary preference.",
        "Include hydration guidance.",
        "Add nutritional balance tips.",
        "No medical advice.",
    ],
    tools=[DuckDuckGoTools()],
    markdown=False
)

fitness_trainer = Agent(
    model=Gemini(id=GEMINI_MODEL_ID),
    description="Creates safe workout plans.",
    instructions=[
        "Include warm-up, workout, and cool-down.",
        "Adjust intensity based on activity level.",
        "Keep exercises home-friendly.",
        "No medical advice or risky exercises.",
    ],
    tools=[DuckDuckGoTools()],
    markdown=False
)

team_lead = Agent(
    model=Gemini(id=GEMINI_MODEL_ID),
    description="Combines meal + workout into a weekly fitness strategy.",
    instructions=[
        "Create a structured weekly schedule.",
        "Explain how diet & exercise work together.",
        "Add rest day recommendations.",
        "End with general safety disclaimer.",
    ],
    markdown=False
)


# -----------------------------------------------------
# ⚙️ HELPER FUNCTIONS
# -----------------------------------------------------
def gen_meal_plan(data: UserInput):
    prompt = f"""
    Create a daily meal plan for:
    Age: {data.age}, Weight: {data.weight}, Height: {data.height},
    Activity Level: {data.activity_level}, Dietary Preference: {data.dietary_preference},
    Fitness Goal: {data.fitness_goal}.
    Include breakfast, lunch, dinner, snacks, hydration tips, and nutrition notes.
    """
    try:
        result = dietary_planner.run(prompt)
        return result.content if hasattr(result, "content") else str(result)
    except ModelProviderError as e:
        return f"Meal Plan Error: {e}"


def gen_workout_plan(data: UserInput):
    prompt = f"""
    Create a workout plan for:
    Age: {data.age}, Weight: {data.weight}, Height: {data.height},
    Activity Level: {data.activity_level}, Fitness Goal: {data.fitness_goal}.
    Include warm-up, main workout, and cool-down.
    Keep exercises beginner-friendly and safe.
    """
    try:
        result = fitness_trainer.run(prompt)
        return result.content if hasattr(result, "content") else str(result)
    except ModelProviderError as e:
        return f"Workout Plan Error: {e}"


def gen_combined_plan(name: str, meal: str, workout: str):
    prompt = f"""
    User: {name}

    Meal Plan:
    {meal}

    Workout Plan:
    {workout}

    Combine these into a weekly schedule.
    Provide daily routine breakdown.
    Add lifestyle tips, rest day suggestions.
    Add a friendly disclaimer.
    """

    try:
        result = team_lead.run(prompt)
        return result.content if hasattr(result, "content") else str(result)
    except ModelProviderError as e:
        return f"Combined Plan Error: {e}"


# -----------------------------------------------------
# 📌 API ROUTE — FRONTEND WILL CALL THIS
# -----------------------------------------------------
@app.post("/generate-plan")
def generate_plan(data: UserInput):
    # 1) Generate diet + workout
    meal = gen_meal_plan(data)
    workout = gen_workout_plan(data)

    # 2) Generate combined strategy
    combined = gen_combined_plan(data.name, meal, workout)

    # 3) Return as JSON
    return {
        "meal_plan": meal,
        "workout_plan": workout,
        "combined_plan": combined
    }


# -----------------------------------------------------
# 🎉 ROOT ENDPOINT
# -----------------------------------------------------
@app.get("/")
def home():
    return {"message": "AI Fitness Backend Running Successfully!"}
