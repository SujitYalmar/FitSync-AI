# 💪 FitSync-AI: AI Health & Fitness Plan Generator

<div align="center">

![GitHub License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-Active-success)
![Kaggle](https://img.shields.io/badge/Kaggle-5--Day%20Agents%20Intensive-blueviolet)

**A Production-Ready Multi-Agent AI System for Personalized Fitness & Nutrition Planning**

[🎯 Overview](#-overview) • [🏗️ Architecture](#-architecture) • [🚀 Quick Start](#-quick-start) • [📊 Tech Stack](#-tech-stack) • [💡 Contributing](#-contributing)

</div>

---

## 🎯 Overview

FitSync-AI is a **multi-agent AI system** that generates personalized, data-driven health and fitness plans. Unlike generic fitness apps, FitSync-AI uses:

✨ **Machine Learning Models** trained on Kaggle fitness datasets  
🤖 **Intelligent Agent Orchestration** for dynamic plan generation  
📊 **Real-time Adaptation** based on user progress and feedback  
🎨 **User-Centric Design** for seamless experience  

**Capstone Project for [Kaggle's 5-Day AI Agents Intensive](https://www.kaggle.com/learn-guide/5-day-agents) Course**

---

## 📋 The Problem It Solves

> **Challenge:** Users track fitness data (steps, calories, workouts) but struggle to convert that data into **personalized, actionable recommendations**. Existing fitness apps provide **generic, static plans** that don't adapt.

**FitSync-AI's Solution:**

1. ✅ **Analyzes** user profiles (age, fitness level, goals, preferences)
2. ✅ **Models** fitness state using ML classifiers trained on real data
3. ✅ **Orchestrates** multi-agent workflows to generate adaptive plans
4. ✅ **Delivers** actionable daily schedules with real-time feedback

---

## 🏗️ System Architecture

```
┌─────────────────┐
│  User Input     │  (Age, Gender, Goals, Activity Data)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  🤖 Profile & Assessment Agent          │  
│  ├─ Data Validation                      │
│  ├─ Feature Extraction                   │
│  └─ ML Model Inference (Fitness Level)  │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  🎯 Plan Generator Agent                │
│  ├─ Workout Planning                     │
│  ├─ Nutrition Suggestions                │
│  └─ 4-Week Personalized Plan             │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  📅 Scheduler & Progress Agent          │
│  ├─ Daily Checklist Generation           │
│  ├─ Progress Tracking                    │
│  └─ Adaptive Recommendations             │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  🎨 Frontend Display                    │
│  ├─ Plan Visualization                   │
│  ├─ Progress Dashboard                   │
│  └─ User Feedback Loop                   │
└─────────────────────────────────────────┘
```

---

## 🤖 Multi-Agent System

### **Agent 1: Profile & Assessment Agent**
- **Role**: Parse user inputs and assess fitness level
- **Tools**: Data validation, feature extraction, fitness scoring
- **Output**: Standardized user profile + fitness classification
- **ML Integration**: Calls trained classifier to predict fitness category

### **Agent 2: Plan Generator Agent**
- **Role**: Create personalized workout & diet plans
- **Tools**: Plan templates, calorie calculator, workout database
- **Output**: Multi-week fitness plan with daily breakdown
- **Logic**: Adjusts intensity based on fitness level and goals

### **Agent 3: Scheduler & Progress Agent**
- **Role**: Convert plans into executable schedules and track progress
- **Tools**: Calendar management, progress tracking, feedback generation
- **Output**: Daily checklist, achievement badges, adaptive recommendations
- **Memory**: Session state for user history and plan adjustments

---

## 📊 ML Model Integration

### **Dataset Source**
- **Source**: Kaggle Fitness Tracking Dataset
- **Features**: Age, Gender, BMI, Activity Level, Weekly Steps, Calories Burned, Sleep Hours, Workout Frequency
- **Target**: Fitness Level Classification (Beginner → Intermediate → Advanced)

### **Model Pipeline**

```
Data → Preprocessing → Feature Engineering → Model Training → Hyperparameter Tuning → Evaluation → Deployment
                        (Normalization)       (Random Forest/     (Grid Search)        (Accuracy,    (As Agent
                                             Gradient Boosting)                       F1-Score)     Tool)
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend Language** | Python 3.8+ |
| **AI Framework** | Google Agent Development Kit (ADK) + Gemini |
| **ML Libraries** | Scikit-learn, Pandas, NumPy |
| **Frontend** | HTML5, Vanilla JavaScript, CSS3 |
| **API** | Flask / FastAPI |
| **Database** | SQLite / Firebase (optional) |
| **Deployment** | Google Cloud Run (optional) |
| **Data Source** | Kaggle Public Datasets |

---

## 📁 Project Structure

```
FitSync-AI/
├── backend/
│   ├── agents/
│   │   ├── profile_agent.py              # User profiling & assessment
│   │   ├── plan_generator_agent.py       # Workout & diet planning
│   │   └── scheduler_agent.py            # Schedule & progress tracking
│   ├── tools/
│   │   ├── data_tools.py                 # Feature extraction, validation
│   │   ├── ml_tools.py                   # Model inference, predictions
│   │   ├── planning_tools.py             # Plan generation logic
│   │   └── schedule_tools.py             # Calendar & reminder tools
│   ├── models/
│   │   ├── fitness_classifier.pkl        # Pre-trained ML model
│   │   └── model_training.py             # Training pipeline
│   ├── api/
│   │   └── main.py                       # Flask API endpoints
│   └── config.py                         # Configuration & API keys
├── frontend/
│   ├── index.html                        # Main UI
│   ├── css/
│   │   └── style.css                     # Styling
│   └── js/
│       └── app.js                        # Frontend logic & API integration
├── data/
│   ├── fitness_data.csv                  # Kaggle dataset
│   └── processed_data.csv                # Preprocessed dataset
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- Kaggle API credentials
- Google Cloud Project with Gemini API enabled

### **Installation**

```bash
# 1️⃣ Clone repository
git clone https://github.com/SujitYalmar/FitSync-AI.git
cd FitSync-AI

# 2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Set up environment variables
echo "GOOGLE_API_KEY=your_key_here" > .env
echo "KAGGLE_USERNAME=your_username" >> .env
echo "KAGGLE_KEY=your_key" >> .env
```

### **Training the Model** (Optional)

```bash
python backend/models/model_training.py
```

This will:
- Download the Kaggle fitness dataset
- Preprocess and normalize features
- Train the fitness classifier
- Save the model as `fitness_classifier.pkl`

### **Running the System**

```bash
# Start backend API
python backend/api/main.py

# Open in browser
http://localhost:5000
```

---

## 📚 How It Works (End-to-End Flow)

```
1. User Onboarding
   └─ Enter profile (age, gender, goals, preferences)

2. Profile Agent Processing
   └─ Validate input → Extract features → Run ML classifier

3. Plan Generation
   └─ Create 4-week personalized workout & meal plan

4. Schedule Creation
   └─ Convert plan to daily executable checklist

5. Frontend Display
   └─ Visualize plan and track daily progress

6. Adaptive Feedback
   └─ Monitor adherence and adapt recommendations
```

---

## 🎓 Course Alignment: Kaggle 5-Day Agents Intensive

| Day | Topic | Implementation |
|-----|-------|----------------|
| **Day 1** | Agent Basics | Multi-agent orchestration framework |
| **Day 2** | Tools & MCP | Custom Python tools for all operations |
| **Day 3** | Context & Memory | Session state & user history tracking |
| **Day 4** | Evaluation | Plan quality scoring & adherence metrics |
| **Day 5** | Production | API design, error handling, scalability |

**Track**: Concierge Agent (Personal AI Fitness Coach) ✅

---

## ✨ Key Features

- 🎯 **Personalized Plans** - Data-driven recommendations based on fitness level
- 🤖 **Multi-Agent Orchestration** - Specialized agents for profiling, planning, scheduling
- 📊 **ML Integration** - Kaggle dataset-trained fitness classifier
- 📈 **Adaptive Feedback** - Progress tracking with dynamic adjustments
- 🛠️ **Tool Ecosystem** - Reusable tools for data processing and planning
- 🔌 **API-First Design** - RESTful backend for easy integration
- 🏗️ **Production Ready** - Error handling, logging, configuration management

---

## 🔄 Future Enhancements

- [ ] **Neural Networks** - Advanced progression prediction
- [ ] **Wearable Integration** - Fitbit, Apple Watch, Garmin APIs
- [ ] **Voice Coach** - Real-time feedback via voice/chat agents
- [ ] **A/B Testing** - Framework for plan effectiveness
- [ ] **Multi-language** - Support for global users
- [ ] **Mobile App** - Flutter cross-platform application
- [ ] **Cloud Deployment** - Google Cloud Run & CI/CD pipelines
- [ ] **Community Features** - Social challenges and leaderboards

---

## 📖 References

- [Kaggle 5-Day AI Agents Intensive](https://www.kaggle.com/learn-guide/5-day-agents)
- [Google Agent Development Kit](https://ai.google.dev/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Scikit-learn Documentation](https://scikit-learn.org/)

---

## 📝 License

This project is licensed under the **MIT License** – see [LICENSE](./LICENSE) file for details.

---

## 👤 Author

**Sujit Yalmar**

- 🔗 [GitHub](https://github.com/SujitYalmar)
- 💼 [LinkedIn](https://linkedin.com/in/sujit-yalmar)
- 📧 Focus: Full-stack AI, Multi-agent systems, Cloud deployment

---

## 💡 Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.

---

<div align="center">

### Built with ❤️ for the Kaggle 5-Day AI Agents Intensive Capstone

⭐ If you found this project helpful, please consider giving it a star!

</div>
