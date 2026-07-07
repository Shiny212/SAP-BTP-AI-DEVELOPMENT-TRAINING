import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of records
n = 1000

education_levels = ["Bachelor", "Master", "PhD"]
job_roles = ["Analyst", "Developer", "Manager", "Data Scientist", "Consultant"]
cities = ["Bangalore", "Hyderabad", "Pune", "Delhi", "Mumbai"]

# Generate data
employee_ids = [f"EMP{1001+i}" for i in range(n)]
ages = np.random.randint(22, 60, n)
experience = np.random.randint(0, 31, n)
education = np.random.choice(education_levels, n, p=[0.55, 0.35, 0.10])
roles = np.random.choice(job_roles, n)
city = np.random.choice(cities, n)
skill_scores = np.random.randint(40, 101, n)
certifications = np.random.randint(0, 8, n)
ratings = np.round(np.random.uniform(2.5, 5.0, n), 1)

# Bonus dictionaries
education_bonus = {
    "Bachelor": 0,
    "Master": 120000,
    "PhD": 250000
}

role_bonus = {
    "Analyst": 50000,
    "Developer": 120000,
    "Manager": 300000,
    "Data Scientist": 220000,
    "Consultant": 140000
}

city_bonus = {
    "Bangalore": 100000,
    "Hyderabad": 70000,
    "Pune": 60000,
    "Delhi": 90000,
    "Mumbai": 110000
}

# Generate salary
salary = (
    300000
    + experience * 85000
    + skill_scores * 5000
    + certifications * 25000
    + ratings * 60000
    + np.array([education_bonus[e] for e in education])
    + np.array([role_bonus[r] for r in roles])
    + np.array([city_bonus[c] for c in city])
    + np.random.normal(0, 70000, n)
)

salary = salary.astype(int)

# Create DataFrame
df = pd.DataFrame({
    "Employee_ID": employee_ids,
    "Age": ages,
    "Years_Experience": experience,
    "Education_Level": education,
    "Job_Role": roles,
    "City": city,
    "Skill_Score": skill_scores,
    "Certifications": certifications,
    "Previous_Company_Rating": ratings,
    "Salary": salary
})

# Save dataset
df.to_csv("employee_salary.csv", index=False)

print("Dataset created successfully!")
print(df.head())
print("\nShape:", df.shape)