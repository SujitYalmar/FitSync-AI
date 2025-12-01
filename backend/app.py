import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.exceptions import ModelProviderError

# -----------------------------------------------------
# 🔑 GOOGLE GEMINI API KEY
# -----------------------------------------------------
os.environ["GOOGLE_API_KEY"] = "AIzaSyBokBtx2TwF_tO5TfZu5FLkUnsK9Dw4R0g"

GEMINI_MODEL_ID = "gemini-2.0-flash-001"

# -----------------------------------------------------
# 🚀 FASTAPI APP
# -----------------------------------------------------
app = FastAPI()

# 👇 IMPORTANT: CORS CONFIG FOR NETLIFY + RENDER
# If you know your Netlify domain, you can replace "*" with:
# origins = ["https://your-site-name.netlify.app"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,  # must be False when using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------
# 📥 REQUEST MODEL
# -----------------------------------------------------
class UserInput(BaseModel):
    name: str
    age: int
    weight: float
    height: float
    activity_level: str
    dietary_preference: str
    fitness_goal: str


# -----------------------------------------------------
# 🤖 AGENTS
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
    markdown=True,  # ✅ let Gemini return Markdown; your frontend uses `marked.parse`
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
# ⚙️ HELPERS
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
    - Exercises should be beginner-friendly and can be done at home or with minimal equipment.
    - Adjust intensity based on activity level.
    - No risky or advanced movements; no medical advice.
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

    Requirements:
    - Use Markdown.
    - Provide a day-wise table or sections (Day 1, Day 2, ...).
    - For each day, mention:
      - Key meals and general structure (not full recipes).
      - Workout focus (e.g., upper body, cardio, rest).
    - Add 3–5 lifestyle tips at the end.
    - Finish with a short, friendly disclaimer that this is not medical advice.
    """
    try:
        result = team_lead.run(prompt)
        return getattr(result, "content", str(result))
    except ModelProviderError as e:
        return f"Combined Plan Error: {e}"


# -----------------------------------------------------
# 📌 MAIN API: /generate-plan
# -----------------------------------------------------
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
        # You can see this in Render logs
        print("❌ Error in /generate-plan:", e)
        raise HTTPException(status_code=500, detail="Internal server error while generating plan")


# -----------------------------------------------------
# 🏠 HEALTH CHECK
# -----------------------------------------------------
@app.get("/")
def home():
    return {"message": "AI Fitness Backend Running Successfully!"}
