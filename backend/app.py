import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from agno.agent import Agent
from agno.models.google import Gemini
# 👇 CHANGE 1: Import Google Search instead of DuckDuckGo
from agno.tools.googlesearch import GoogleSearchTools
from agno.exceptions import ModelProviderError

# -----------------------------------------------------
# 🔑 API KEYS (Load these securely!)
# -----------------------------------------------------
# ⚠️ REPLACE WITH YOUR REAL KEYS
os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY_HERE"
os.environ["GOOGLE_CSE_ID"] = "YOUR_SEARCH_ENGINE_ID_HERE" # 👈 PASTE ID FROM STEP 1

GEMINI_MODEL_ID = "gemini-2.0-flash-001"

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    name: str
    age: int
    weight: float
    height: float
    activity_level: str
    dietary_preference: str
    fitness_goal: str

# -----------------------------------------------------
# 🤖 AGENTS (Updated with Google Tools)
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
    # 👇 CHANGE 2: Use Google Search Tool
    tools=[GoogleSearchTools()], 
    markdown=True,
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
    # 👇 CHANGE 3: Use Google Search Tool
    tools=[GoogleSearchTools()],
    markdown=True,
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
    markdown=True,
)

# -----------------------------------------------------
# ⚙️ HELPERS (Real Logic Restored)
# -----------------------------------------------------
def gen_meal_plan(data: UserInput) -> str:
    prompt = f"""
    Create a daily meal plan for:
    Name: {data.name}
    Age: {data.age}, Weight: {data.weight} kg, Height: {data.height} cm,
    Activity Level: {data.activity_level}, Dietary Preference: {data.dietary_preference},
    Fitness Goal: {data.fitness_goal}.

    Requirements:
    - Use clear Markdown.
    - Include: breakfast, lunch, dinner, and 1–2 snacks.
    - Add hydration tips.
    - Brief macro or nutrition notes.
    - No medical advice or diagnosis.
    """
    try:
        # This will now use Google Search if needed
        result = dietary_planner.run(prompt)
        return getattr(result, "content", str(result))
    except ModelProviderError as e:
        return f"Meal Plan Error: {e}"

def gen_workout_plan(data: UserInput) -> str:
    prompt = f"""
    Create a workout plan for:
    Name: {data.name}
    Age: {data.age}, Weight: {data.weight} kg, Height: {data.height} cm,
    Activity Level: {data.activity_level}, Fitness Goal: {data.fitness_goal}.

    Requirements:
    - Use clear Markdown with headings and bullet points.
    - Include: warm-up, main workout, and cool-down.
    - Exercises should be beginner-friendly.
    - Adjust intensity based on activity level.
    - No risky movements; no medical advice.
    """
    try:
        result = fitness_trainer.run(prompt)
        return getattr(result, "content", str(result))
    except ModelProviderError as e:
        return f"Workout Plan Error: {e}"

def gen_combined_plan(name: str, meal: str, workout: str) -> str:
    prompt = f"""
    User: {name}

    --- MEAL PLAN ---
    {meal}

    --- WORKOUT PLAN ---
    {workout}

    Combine these into a 7-day weekly plan.
    """
    try:
        result = team_lead.run(prompt)
        return getattr(result, "content", str(result))
    except ModelProviderError as e:
        return f"Combined Plan Error: {e}"

@app.post("/generate-plan")
def generate_plan(data: UserInput):
    try:
        meal = gen_meal_plan(data)
        workout = gen_workout_plan(data)
        combined = gen_combined_plan(data.name, meal, workout)

        return {
            "meal_plan": meal,
            "workout_plan": workout,
            "combined_plan": combined,
        }
    except Exception as e:
        print("❌ Error in /generate-plan:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
def home():
    return {"message": "AI Fitness Backend Running Successfully!"}