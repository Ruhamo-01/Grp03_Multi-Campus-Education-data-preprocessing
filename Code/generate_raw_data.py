import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

os.makedirs("raw_data", exist_ok=True)

# ----------------------------
# Helper functions
# ----------------------------

first_names = ["Alice", "Bob", "Jean", "Aline", "Eric", "Grace", "Patrick", "Claudine"]
last_names = ["Uwimana", "Niyonsenga", "Mukamana", "Habimana", "Nsabimana"]

programs = ["Computer Science", "Information Tech", "Data Science", "Software Eng"]

courses = [
    ("CS101", "Programming", 3),
    ("CS102", "Databases", 4),
    ("CS103", "Cyber security", 3),
    ("CS104", "Machine Learning", 4),
]

assessment_types = ["Summative", "CAT", "Formative"]

campuses = [
    ("KIG-25", "Kigali"),
    ("HUY-26", "Huye"),
    ("MUS-27", "Musanze"),
]

# Random date generator
def random_date():
    start = datetime(2023, 1, 1)
    return start + timedelta(days=random.randint(0, 700))

# Mixed date format function (NEW)
def random_date_format(date):
    formats = [
        "%Y-%m-%d",        # 2024-02-15
        "%d/%m/%Y",        # 15/02/2024
        "%m-%d-%Y",        # 02-15-2024
        "%b %d, %Y",       # Feb 15, 2024
        "%d %B %Y"         # 15 February 2024
    ]
    return date.strftime(random.choice(formats))


# ----------------------------
# Generate datasets per campus
# ----------------------------

for campus_id, campus_name in campuses:

    # STUDENTS DATASET
    students = []
    for i in range(40):

        sid = f"{campus_id}{100+i}"

        students.append({
            "Student_ID": sid,
            "Full_Name": random.choice(first_names) + " " + random.choice(last_names),
            "Gender": random.choice(["Male", "Female", None]),  # missing values
            "DOB": random.choice([random_date_format(random_date()), None]),
            "Program": random.choice(programs).upper() if i % 5 == 0 else random.choice(programs),
            "Level": random.choice([1, 2, 3]),
            "Intake_Year": random.choice([2022, 2023, 2024])
        })

    df_students = pd.DataFrame(students)

    # Add duplicate intentionally
    df_students = pd.concat([df_students, df_students.iloc[[5]]])

    df_students.to_csv(f"raw_data/{campus_name}_students.csv", index=False)

    # COURSES DATASET
    df_courses = pd.DataFrame(courses, columns=["Course_Code", "Course_Title", "Credits"])
    df_courses["Campus_ID"] = campus_id

    # Introduce inconsistent course code format
    df_courses.loc[1, "Course_Code"] = "CS-102"

    df_courses.to_csv(f"raw_data/{campus_name}_courses.csv", index=False)

    # ASSESSMENTS DATASET
    assessments = []
    for sid in df_students["Student_ID"].sample(50, replace=True):

        code, title, credit = random.choice(courses)

        mark = random.choice([
            random.randint(40, 90),
            105,     # outlier (>100)
            -5,      # invalid negative mark
            None
        ])

        assessments.append({
            "Student_ID": sid,
            "Course_Code": code,
            "Assessment_Type": random.choice(assessment_types),
            "Mark": mark,
            "Assessment_Date": random_date_format(random_date()),
            "Academic_Year": "2024/2025",
            "Semester": random.choice([1, 2]),
            "Attendance_Rate": random.choice([0.8, 0.6, 1.1, None])
        })

    df_assess = pd.DataFrame(assessments)

    df_assess.to_csv(f"raw_data/{campus_name}_assessments.csv", index=False)

print("Raw datasets generated successfully!")