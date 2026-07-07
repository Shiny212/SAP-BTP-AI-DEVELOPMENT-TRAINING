import pandas as pd
import numpy as np

# For reproducibility
np.random.seed(42)

# Number of records
n = 1000

# Generate data
data = {
    "Customer_ID": [f"CUST{1000+i}" for i in range(n)],
    "Age": np.random.randint(21, 60, n),
    "Monthly_Income": np.random.randint(20000, 100000, n),
    "Credit_Score": np.random.randint(300, 850, n),
    "Loan_Amount": np.random.randint(100000, 1000000, n),
    "Loan_Tenure_Months": np.random.choice([12, 24, 36, 48, 60], n),
    "Existing_EMI": np.random.randint(1000, 30000, n),
    "Employment_Type": np.random.choice(
        ["Salaried", "Self-employed", "Business", "Unemployed"], n
    ),
    "Education_Level": np.random.choice(
        ["Graduate", "Postgraduate", "Diploma", "School"], n
    ),
    "Marital_Status": np.random.choice(
        ["Single", "Married"], n
    ),
    "Dependents": np.random.randint(0, 5, n),
    "Previous_Default": np.random.choice(
        ["Yes", "No"], n
    )
}

df = pd.DataFrame(data)

# Risk Score Calculation
risk_score = (
    (df["Credit_Score"] < 600).astype(int) * 3 +
    (df["Monthly_Income"] < 40000).astype(int) * 2 +
    (df["Loan_Amount"] > 700000).astype(int) * 2 +
    (df["Existing_EMI"] > 15000).astype(int) * 2 +
    (df["Previous_Default"] == "Yes").astype(int) * 3 +
    (df["Employment_Type"] == "Unemployed").astype(int) * 2
)

# Final Target Variable
df["Loan_Default"] = np.where(risk_score >= 6, 1, 0)

# Save dataset
df.to_csv("dataset/loan_default_dataset.csv", index=False)

print("Dataset created successfully!")
print(df.head())