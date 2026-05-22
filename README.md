# 🎓 Smart Learning Analytics Hub
## AI-Powered Student Performance Analysis System

---

## 📁 Project Structure

```
smart_learning_hub/
│
├── run_all.py                  ← ← ← Run this file only! It runs everything
│
├── data/
│   ├── generate_dataset.py     ← Generates data for 500 students
│   └── student_performance.csv ← Dataset (auto-generated)
│
├── project1_pipeline/
│   └── project1_pipeline.py    ← Full pipeline from data to prediction
│
├── project2_regression/
│   └── regression_model.py     ← Predicts student's numeric grade
│
├── project3_classification/
│   └── classification_model.py ← Classifies student (at_risk/average/strong)
│
├── project4_llm_agent/
│   └── study_agent.py          ← AI-powered smart study assistant
│
├── project5_real_data/
│   └── project5_analysis.py    ← Real-world data analysis
│
├── project6_visualization/
│   └── visualization_dashboard.py ← Professional charts & dashboards
│
├── models/                     ← Saved ML models (auto-created)
└── outputs/                    ← All output files (images & reports)
```

---

## 🚀 How to Run the Project

### Step 1 — Install dependencies (one time only)
```bash
pip install pandas numpy scikit-learn matplotlib seaborn joblib
```

### Step 2 — Run everything
```bash
python run_all.py
```

**That's it! It will do everything automatically.**

---

## 📊 What Happens When You Run It?

| Stage | Project | What Happens |
|-------|---------|--------------|
| 0 | Data | Generate data for 500 students |
| 1 | Project 5 | Analyze data and plot heatmap |
| 2 | Project 1 | Full pipeline and save model |
| 3 | Project 2 | Train 4 Regression models and compare |
| 4 | Project 3 | Train 4 Classification models and compare |
| 5 | Project 4 | Demo of the AI Agent |
| 6 | Project 6 | Draw 4 professional dashboards |
| 7 | Project 7 | Analyze a new student and display results |

---

## 📁 Output Files in outputs/

```
outputs/
├── cleaned_dataset.csv          ← Cleaned dataset
│
├── p5_correlation_heatmap.png   ← Project 5: Correlations between features
├── p5_score_distribution.png    ← Project 5: Score distribution
│
├── p1_actual_vs_predicted.png   ← Project 1: Predictions vs actual values
│
├── p6_fig1_overview.png         ← Project 6: Dataset overview
├── p6_fig2_patterns.png         ← Project 6: Patterns and relationships
├── p6_fig3_models.png           ← Project 6: Model results
├── p6_fig4_insights.png         ← Project 6: Insights and recommendations
│
└── p7_student_dashboard.png     ← Project 7: New student analysis
```

---

## 🔧 Running a Single Project Separately

If you want to run just one project:

```bash
# Generate data first (required before anything else)
cd data && python generate_dataset.py && cd ..

# Run Project 1 separately
cd project1_pipeline
python project1_pipeline.py

# Run Project 2 separately
cd project2_regression
python regression_model.py

# And so on...
```

---

## 🤖 Enabling the AI Agent (Project 4)

Project 4 runs without an API key in "demo mode".
To use the real AI:

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create an API Key
3. Run:
```bash
export ANTHROPIC_API_KEY=your_key_here
python run_all.py
```

---

## 📚 Glossary for Beginners

| Term | Simple Explanation |
|------|-------------------|
| **Regression** | Model predicts a number (e.g. grade from 0–100) |
| **Classification** | Model predicts a category (e.g. at_risk / average / strong) |
| **R²** | Describes model accuracy — closer to 1 is better |
| **MAE** | Average prediction error — smaller is better |
| **Feature** | Any input given to the model (study hours, attendance rate...) |
| **Pipeline** | A chain of connected steps from data cleaning to prediction |
| **Confusion Matrix** | A table showing where the model made classification errors |
