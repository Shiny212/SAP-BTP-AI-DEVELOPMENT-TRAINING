import pandas as pd
import joblib

# Load model
model = joblib.load("models/best_random_forest.pkl")

# New Customer
new_customer = pd.DataFrame({

    "Customer_ID":["CUST9999"],

    "Age":[35],

    "Monthly_Income":[40000],

    "Credit_Score":[590],

    "Loan_Amount":[800000],

    "Loan_Tenure_Months":[48],

    "Existing_EMI":[12000],

    "Employment_Type":["Self-employed"],

    "Education_Level":["Graduate"],

    "Marital_Status":["Married"],

    "Dependents":[2],

    "Previous_Default":["Yes"]

})

prediction = model.predict(new_customer)

probability = model.predict_proba(new_customer)

print("Prediction:", prediction[0])

print("Probability:", probability)

if prediction[0] == 1:
    print("\nLoan Default Risk : HIGH")
else:
    print("\nLoan Default Risk : LOW")