import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import joblib
# Load dataset
df = pd.read_csv("employee_salary.csv")

print("Dataset Loaded Successfully!\n")

print("First 5 Records:")
print(df.head())

print("\nShape of Dataset:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)

print("\nSummary Statistics:")
print(df.describe())

print("\nMissing Values:")
print(df.isnull().sum())



# Salary Distribution
plt.figure(figsize=(8,5))
sns.histplot(df["Salary"], bins=30, kde=True)
plt.title("Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Count")
plt.show()


# Experience vs Salary
plt.figure(figsize=(8,5))
sns.scatterplot(
    data=df,
    x="Years_Experience",
    y="Salary"
)
plt.title("Years of Experience vs Salary")
plt.show()


# Education Level vs Salary
plt.figure(figsize=(8,5))
sns.boxplot(
    data=df,
    x="Education_Level",
    y="Salary"
)
plt.title("Education Level vs Salary")
plt.show()


# Job Role vs Salary
plt.figure(figsize=(10,5))
sns.boxplot(
    data=df,
    x="Job_Role",
    y="Salary"
)
plt.xticks(rotation=30)
plt.title("Job Role vs Salary")
plt.show()


# City-wise Salary
plt.figure(figsize=(8,5))
sns.boxplot(
    data=df,
    x="City",
    y="Salary"
)
plt.title("City-wise Salary")
plt.show()


# Correlation Heatmap
plt.figure(figsize=(8,6))

numeric_df = df.select_dtypes(include=np.number)

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")
plt.show()


# Salary Outliers
plt.figure(figsize=(6,5))
sns.boxplot(y=df["Salary"])
plt.title("Salary Outliers")
plt.show()


# Input features and target variable
X = df.drop(columns=["Employee_ID", "Salary"])
y = df["Salary"]


# Numerical columns
numeric_features = [
    "Age",
    "Years_Experience",
    "Skill_Score",
    "Certifications",
    "Previous_Company_Rating"
]

# Categorical columns
categorical_features = [
    "Education_Level",
    "Job_Role",
    "City"
]


# Numeric preprocessing
numeric_transformer = Pipeline([
    ("scaler", StandardScaler())
])


# Categorical preprocessing
categorical_transformer = Pipeline([
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])


# Combine preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("Training Data Shape:", X_train.shape)
print("Testing Data Shape:", X_test.shape)



# Create regression models
models = {
    "Dummy Regressor": DummyRegressor(),

    "Linear Regression": LinearRegression(),

    "Ridge Regression": Ridge(),

    "Lasso Regression": Lasso(),

    "Random Forest": RandomForestRegressor(
        random_state=42
    )
}


# Store results
results = []

for name, model in models.items():

    # Create pipeline
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    # Train
    pipeline.fit(X_train, y_train)

    # Predict
    y_pred = pipeline.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    r2 = r2_score(y_test, y_pred)

    # Save results
    results.append([name, mae, rmse, r2])

    print(f"\n{name}")
    print("-" * 30)
    print("MAE :", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R²  :", round(r2, 4))



comparison = pd.DataFrame(
    results,
    columns=[
        "Model",
        "MAE",
        "RMSE",
        "R2 Score"
    ]
)

comparison = comparison.sort_values(
    by="R2 Score",
    ascending=False
)

print("\nModel Comparison")
print(comparison)



best_model_name = comparison.iloc[0]["Model"]

print("\nBest Model:", best_model_name)



# Random Forest Pipeline
rf_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(random_state=42))
])



# Hyperparameter Grid
param_grid = {
    "model__n_estimators": [50, 100, 200],
    "model__max_depth": [5, 10, 15],
    "model__min_samples_split": [2, 5, 10]
}



grid_search = GridSearchCV(
    estimator=rf_pipeline,
    param_grid=param_grid,
    cv=5,
    scoring="r2",
    n_jobs=-1
)

grid_search.fit(X_train, y_train)



print("\nBest Parameters:")
print(grid_search.best_params_)

print("\nBest Cross Validation Score:")
print(grid_search.best_score_)



best_model = grid_search.best_estimator_

predictions = best_model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("\nFinal Model Performance")
print("-------------------------")
print("MAE :", round(mae,2))
print("RMSE:", round(rmse,2))
print("R2 :", round(r2,4))



# Extract preprocessing and model
preprocessor = best_model.named_steps["preprocessor"]
model = best_model.named_steps["model"]

# Original numeric feature names
numeric_names = numeric_features

# Encoded categorical feature names
encoder = preprocessor.named_transformers_["cat"].named_steps["encoder"]

categorical_names = encoder.get_feature_names_out(categorical_features)

# Final feature names
feature_names = list(numeric_names) + list(categorical_names)

# Importance DataFrame
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 10 Important Features")
print(importance_df.head(10))



import matplotlib.pyplot as plt

# Top 10 important features
top10 = importance_df.head(10)

plt.figure(figsize=(10,6))
plt.barh(top10["Feature"], top10["Importance"])
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.title("Top 10 Feature Importances (Tuned Random Forest)")
plt.gca().invert_yaxis()  # Highest importance at the top
plt.tight_layout()
plt.show()


new_employee = pd.DataFrame({
    "Age": [30],
    "Years_Experience": [6],
    "Education_Level": ["Master"],
    "Job_Role": ["Data Scientist"],
    "City": ["Bangalore"],
    "Skill_Score": [85],
    "Certifications": [3],
    "Previous_Company_Rating": [4.2]
})

predicted_salary = best_model.predict(new_employee)

print("\nPredicted Salary")
print(f"₹{predicted_salary[0]:,.2f}")



joblib.dump(best_model, "employee_salary_model.pkl")

print("\nModel Saved Successfully!")



loaded_model = joblib.load("employee_salary_model.pkl")

prediction = loaded_model.predict(new_employee)

print("\nPrediction Using Loaded Model")
print(f"₹{prediction[0]:,.2f}")