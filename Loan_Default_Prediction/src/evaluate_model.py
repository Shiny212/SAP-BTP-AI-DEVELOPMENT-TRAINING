import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    RocCurveDisplay
)

# ==========================
# Load Dataset
# ==========================

df = pd.read_csv("dataset/loan_default_dataset.csv")

# Features and Target
X = df.drop("Loan_Default", axis=1)
y = df["Loan_Default"]

# Numerical and Categorical Columns
numerical_columns = X.select_dtypes(include=["int64", "float64"]).columns
categorical_columns = X.select_dtypes(include=["object"]).columns

# ==========================
# Preprocessing
# ==========================

numerical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numerical_pipeline, numerical_columns),
    ("cat", categorical_pipeline, categorical_columns)
])

# ==========================
# Train Test Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)

# ==========================
# Models
# ==========================

models = {
    "Dummy Classifier": DummyClassifier(strategy="most_frequent"),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42)
}

results = []

# ==========================
# Train and Evaluate
# ==========================

for name, model in models.items():

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_prob)

    results.append([
        name,
        accuracy,
        precision,
        recall,
        f1,
        roc_auc
    ])

    print("\n==============================")
    print(name)
    print("==============================")

    print(classification_report(y_test, y_pred))

    # ==========================
    # Confusion Matrix
    # ==========================

    cm = confusion_matrix(y_test, y_pred)

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["Safe", "Default"]
    )

    disp.plot(cmap="Blues")

    plt.title(f"Confusion Matrix - {name}")

    plt.show()

    # ==========================
    # ROC Curve (Only Random Forest)
    # ==========================

    if name == "Random Forest":

        plt.figure(figsize=(8,6))

        RocCurveDisplay.from_estimator(
            pipeline,
            X_test,
            y_test
        )

        plt.plot(
            [0,1],
            [0,1],
            linestyle="--",
            color="red",
            label="Random Guess"
        )

        plt.title("ROC Curve - Random Forest")

        plt.legend()

        plt.show()

# ==========================
# Model Comparison
# ==========================

comparison = pd.DataFrame(
    results,
    columns=[
        "Model",
        "Accuracy",
        "Precision",
        "Recall",
        "F1-Score",
        "ROC-AUC"
    ]
)

print("\n==============================")
print("Model Comparison")
print("==============================")

print(comparison)

# ==========================
# Best Model
# ==========================

best_model = comparison.loc[
    comparison["ROC-AUC"].idxmax()
]

print("\n==============================")
print("Best Model Based on ROC-AUC")
print("==============================")

print(best_model)