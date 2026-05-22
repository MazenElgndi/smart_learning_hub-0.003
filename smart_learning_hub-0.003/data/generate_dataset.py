"""
generate_dataset.py
-------------------
Generates a realistic student performance dataset for Egyptian public high schools.

Dataset covers:
  - 3 academic years: Grade 10 (First Secondary), Grade 11 (Second Secondary), Grade 12 (Third Secondary)
  - 1,500 students per year → 4,500 students total
  - 10 real Egyptian public high schools (based on actual school names in Cairo, Giza, Alexandria)
  - ~450 students per school (realistic class sizes for Egyptian secondary education)

Run this FIRST to generate the data file used in all other scripts.
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

# ─── School List (real Egyptian public high schools) ────────────────────────
SCHOOLS = [
    # School Name                               , Governorate , City
    ("Al-Orman High School",                     "Cairo",      "Giza"),
    ("Zamalek Secondary School",                 "Cairo",      "Cairo"),
    ("Heliopolis Secondary School for Boys",     "Cairo",      "Cairo"),
    ("Maadi Secondary School",                   "Cairo",      "Cairo"),
    ("Ahmed Orabi Secondary School",             "Giza",       "Giza"),
    ("Smouha Secondary School",                  "Alexandria", "Alexandria"),
    ("Al-Raml Secondary School",                 "Alexandria", "Alexandria"),
    ("Port Said Secondary School",               "Port Said",  "Port Said"),
    ("Mansoura Secondary School for Boys",       "Dakahlia",   "Mansoura"),
    ("Assiut Secondary School",                  "Assiut",     "Assiut"),
]

GRADES = {
    10: "Grade 10 - First Secondary",
    11: "Grade 11 - Second Secondary",
    12: "Grade 12 - Third Secondary",
}

STUDENTS_PER_YEAR = 1500   # exactly 1,500 per academic year
STUDENTS_PER_SCHOOL_PER_YEAR = STUDENTS_PER_YEAR // len(SCHOOLS)   # 150

# ─── Helper: generate features for N students with school-level variation ───
def generate_school_cohort(school_idx, grade, n, seed_offset):
    rng = np.random.RandomState(42 + seed_offset)

    school_name, gov, city = SCHOOLS[school_idx]

    # School quality factor: top urban schools score slightly higher on average
    quality = [0.10, 0.05, 0.08, 0.06, 0.02, 0.04, 0.01, -0.02, -0.03, -0.05][school_idx]

    # Grade difficulty factor: Grade 12 (Thanaweya Amma) is hardest
    grade_difficulty = {10: 0.05, 11: 0.0, 12: -0.06}[grade]

    base_study   = 4.5 + quality * 3 + grade_difficulty * 2
    base_attend  = 78  + quality * 8 + grade_difficulty * 3

    study_hours       = rng.normal(loc=base_study,  scale=1.4, size=n).clip(0, 12)
    attendance_pct    = rng.normal(loc=base_attend, scale=13,  size=n).clip(0, 100)
    assignments_done  = rng.randint(0, 20, size=n)
    quizzes_solved    = rng.randint(0, 15, size=n)
    login_frequency   = rng.randint(1, 30, size=n)
    missed_deadlines  = rng.randint(0, 10, size=n)
    retries           = rng.randint(0, 5,  size=n)
    revision_sessions = rng.randint(0, 8,  size=n)
    time_per_task     = rng.normal(loc=30, scale=10, size=n).clip(5, 90)

    # Final score formula (realistic)
    raw_score = (
        study_hours       * 3.5  +
        attendance_pct    * 0.3  +
        assignments_done  * 1.2  +
        quizzes_solved    * 1.5  -
        missed_deadlines  * 2.0  +
        revision_sessions * 2.0  +
        rng.normal(0, 5, n)
    )

    # Normalize per cohort to 0–100
    rng2 = np.random.RandomState(99 + seed_offset)
    noise_shift = rng2.normal(0, 3)   # slight school-level shift
    score = ((raw_score - raw_score.min()) / (raw_score.max() - raw_score.min()) * 100 + noise_shift)
    score = score.clip(0, 100).round(1)

    # Add missing values (5% each in study_hours, attendance, quizzes_solved)
    study_hours    = study_hours.astype(float)
    attendance_pct = attendance_pct.astype(float)
    quizzes_solved = quizzes_solved.astype(float)
    for arr in [study_hours, attendance_pct, quizzes_solved]:
        mask = rng.choice([True, False], size=n, p=[0.05, 0.95])
        arr[mask] = np.nan

    def classify(s):
        if s < 40:   return "at_risk"
        elif s < 70: return "average"
        else:        return "strong"

    # Unique student IDs: G<grade>_S<school_idx+1>_<seq>
    ids = [f"G{grade}_S{school_idx+1:02d}_{str(i+1).zfill(4)}" for i in range(n)]

    df = pd.DataFrame({
        "student_id":        ids,
        "school_name":       school_name,
        "governorate":       gov,
        "city":              city,
        "grade":             grade,
        "grade_label":       GRADES[grade],
        "study_hours":       study_hours.round(2),
        "attendance_pct":    attendance_pct.round(1),
        "assignments_done":  assignments_done,
        "quizzes_solved":    quizzes_solved,
        "login_frequency":   login_frequency,
        "missed_deadlines":  missed_deadlines,
        "retries":           retries,
        "revision_sessions": revision_sessions,
        "time_per_task_min": time_per_task.round(1),
        "final_score":       score,
        "learner_status":    [classify(s) for s in score],
    })

    return df


# ─── Main: generate all cohorts ─────────────────────────────────────────────
all_dfs = []
for grade in [10, 11, 12]:
    for s_idx, (school_name, gov, city) in enumerate(SCHOOLS):
        cohort = generate_school_cohort(
            school_idx=s_idx,
            grade=grade,
            n=STUDENTS_PER_SCHOOL_PER_YEAR,
            seed_offset=s_idx * 100 + grade
        )
        all_dfs.append(cohort)

df_full = pd.concat(all_dfs, ignore_index=True)

# Shuffle rows so grades/schools are interleaved (more realistic)
df_full = df_full.sample(frac=1, random_state=42).reset_index(drop=True)

# ─── Save ───────────────────────────────────────────────────────────────────
out_path = os.path.join(os.path.dirname(__file__), "student_performance.csv")
df_full.to_csv(out_path, index=False)

print(f"✅ Dataset saved → {out_path}")
print(f"   Total students : {len(df_full):,}")
print(f"   Columns        : {df_full.shape[1]}")
print(f"\n   Students per grade:")
for g, lbl in GRADES.items():
    n = (df_full["grade"] == g).sum()
    print(f"     {lbl}: {n:,} students")

print(f"\n   Students per school (all grades combined):")
for school, _, _ in SCHOOLS:
    n = (df_full["school_name"] == school).sum()
    print(f"     {school}: {n:,} students")

print(f"\n   Learner status distribution:")
for status, cnt in df_full["learner_status"].value_counts().items():
    print(f"     {status}: {cnt:,} ({cnt/len(df_full)*100:.1f}%)")

print(f"\nSample rows:")
print(df_full[["student_id","school_name","grade_label","final_score","learner_status"]].head(6).to_string(index=False))
