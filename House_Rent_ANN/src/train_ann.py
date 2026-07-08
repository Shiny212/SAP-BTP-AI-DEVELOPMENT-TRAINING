import os
# Hide TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import tensorflow as tf
# Hide TensorFlow Python logs
tf.get_logger().setLevel("ERROR")
# ==========================================
# TensorFlow / Keras Imports
# ==========================================

import tensorflow as tf

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import (
    Dense,
    Dropout,
    Input
)

from tensorflow.keras.callbacks import EarlyStopping
from sklearn.dummy import DummyRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import numpy as np
from sklearn.model_selection import train_test_split

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline
# Create plots folder if it doesn't exist
os.makedirs("../plots", exist_ok=True)


# Load dataset
df = pd.read_csv("../data/house_rent.csv")


print("=" * 60)
print("HOUSE RENT DATASET INFORMATION")
print("=" * 60)

print("\nShape of Dataset:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nFirst 5 Records:")
print(df.head())

print("\nLast 5 Records:")
print(df.tail())

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nSummary Statistics:")
print(df.describe())


print("\nNumerical Columns:")
print(df.select_dtypes(include=np.number).columns)

print("\nCategorical Columns:")
print(df.select_dtypes(include="object").columns)


plt.figure(figsize=(8,5))

sns.histplot(
    data=df,
    x="Monthly_Rent",
    bins=30,
    kde=True
)

plt.title("Monthly Rent Distribution")

plt.savefig("../plots/rent_distribution.png")

plt.show()



plt.figure(figsize=(8,5))

sns.barplot(
    data=df,
    x="City",
    y="Monthly_Rent"
)

plt.title("Average Rent by City")

plt.xticks(rotation=45)

plt.savefig("../plots/rent_by_city.png")

plt.show()



plt.figure(figsize=(8,5))

sns.boxplot(
    data=df,
    x="Property_Type",
    y="Monthly_Rent"
)

plt.title("Rent by Property Type")

plt.xticks(rotation=20)

plt.savefig("../plots/property_type_vs_rent.png")

plt.show()



plt.figure(figsize=(8,5))

sns.boxplot(
    data=df,
    x="BHK",
    y="Monthly_Rent"
)

plt.title("Rent by BHK")

plt.savefig("../plots/bhk_vs_rent.png")

plt.show()



plt.figure(figsize=(8,5))

sns.scatterplot(
    data=df,
    x="Size_sqft",
    y="Monthly_Rent"
)

plt.title("Property Size vs Rent")

plt.savefig("../plots/size_vs_rent.png")

plt.show()



plt.figure(figsize=(8,5))

sns.boxplot(
    data=df,
    x="Furnishing_Status",
    y="Monthly_Rent"
)

plt.title("Furnishing Status vs Rent")

plt.savefig("../plots/furnishing_vs_rent.png")

plt.show()



plt.figure(figsize=(8,5))

sns.scatterplot(
    data=df,
    x="Distance_to_Metro_km",
    y="Monthly_Rent"
)

plt.title("Distance to Metro vs Rent")

plt.savefig("../plots/metro_vs_rent.png")

plt.show()



numeric_df = df.select_dtypes(include=np.number)

plt.figure(figsize=(10,8))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")

plt.savefig("../plots/correlation_heatmap.png")

plt.show()



# -----------------------------
# Features and Target
# -----------------------------

X = df.drop(columns=["Monthly_Rent"])

y = df["Monthly_Rent"]



X = X.drop(columns=["Property_ID"])


numerical_columns = [

    "BHK",

    "Size_sqft",

    "Bathroom_Count",

    "Floor_Number",

    "Total_Floors",

    "Distance_to_Metro_km",

    "Property_Age_Years"

]



categorical_columns = [

    "City",

    "Area_Locality",

    "Property_Type",

    "Furnishing_Status",

    "Parking_Available"

]



numerical_pipeline = Pipeline(

    steps=[

        (

            "imputer",

            SimpleImputer(strategy="median")

        ),

        (

            "scaler",

            StandardScaler()

        )

    ]

)



categorical_pipeline = Pipeline(

    steps=[

        (

            "imputer",

            SimpleImputer(strategy="most_frequent")

        ),

        (

            "encoder",

            OneHotEncoder(

                handle_unknown="ignore"

            )

        )

    ]

)



preprocessor = ColumnTransformer(

    transformers=[

        (

            "num",

            numerical_pipeline,

            numerical_columns

        ),

        (

            "cat",

            categorical_pipeline,

            categorical_columns

        )

    ]

)




X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)



X_train_processed = preprocessor.fit_transform(

    X_train

)

X_test_processed = preprocessor.transform(

    X_test

)



print()

print("Training Shape")

print(X_train_processed.shape)

print()

print("Testing Shape")

print(X_test_processed.shape)


print()

print("Preprocessing Completed Successfully")



# ----------------------------------
# Baseline Model
# ----------------------------------

dummy_model = DummyRegressor(strategy="mean")


dummy_model.fit(
    X_train_processed,
    y_train
)



dummy_predictions = dummy_model.predict(
    X_test_processed
)



dummy_mae = mean_absolute_error(
    y_test,
    dummy_predictions
)




dummy_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        dummy_predictions
    )
)




dummy_r2 = r2_score(
    y_test,
    dummy_predictions
)



print("\n" + "=" * 50)
print("BASELINE MODEL RESULTS")
print("=" * 50)

print(f"MAE  : {dummy_mae:.2f}")

print(f"RMSE : {dummy_rmse:.2f}")

print(f"R²   : {dummy_r2:.4f}")



# ==========================================
# Build ANN Model
# ==========================================

model = Sequential([
    Input(shape=(X_train_processed.shape[1],)),
    Dense(128, activation="relu"),
    Dropout(0.3),
    Dense(64, activation="relu"),
    Dropout(0.2),
    Dense(32, activation="relu"),
    Dense(1)
])

# ==========================================
# Display Model Summary
# ==========================================

print("\n" + "=" * 60)
print("ANN MODEL SUMMARY")
print("=" * 60)

model.summary()

# ==========================================
# Compile Model
# ==========================================

model.compile(
    optimizer="adam",
    loss="mse",
    metrics=["mae"]
)

# ==========================================
# Early Stopping
# ==========================================

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=10,
    restore_best_weights=True
)

# ==========================================
# Train ANN
# ==========================================

history = model.fit(
    X_train_processed,
    y_train,
    validation_split=0.2,
    epochs=100,
    batch_size=32,
    callbacks=[early_stop],
    verbose=1
)

# ==========================================
# Predict on Test Data
# ==========================================

ann_predictions = model.predict(X_test_processed)

ann_predictions = ann_predictions.flatten()

# ==========================================
# ANN Evaluation
# ==========================================

ann_mae = mean_absolute_error(
    y_test,
    ann_predictions
)

ann_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        ann_predictions
    )
)

ann_r2 = r2_score(
    y_test,
    ann_predictions
)

print("\n" + "=" * 50)
print("ANN MODEL RESULTS")
print("=" * 50)

print(f"MAE  : {ann_mae:.2f}")
print(f"RMSE : {ann_rmse:.2f}")
print(f"R²   : {ann_r2:.4f}")

# ==========================================
# Training vs Validation Loss
# ==========================================

plt.figure(figsize=(8,5))

plt.plot(
    history.history["loss"],
    label="Training Loss"
)

plt.plot(
    history.history["val_loss"],
    label="Validation Loss"
)

plt.title("Training vs Validation Loss")

plt.xlabel("Epoch")

plt.ylabel("Loss")

plt.legend()

plt.savefig("../plots/loss_curve.png")

plt.show()

# ==========================================
# Training vs Validation MAE
# ==========================================

plt.figure(figsize=(8,5))

plt.plot(
    history.history["mae"],
    label="Training MAE"
)

plt.plot(
    history.history["val_mae"],
    label="Validation MAE"
)

plt.title("Training vs Validation MAE")

plt.xlabel("Epoch")

plt.ylabel("MAE")

plt.legend()

plt.savefig("../plots/mae_curve.png")

plt.show()

# ==========================================
# Save Model
# ==========================================

os.makedirs("../models", exist_ok=True)

model.save("../models/house_rent_ann.keras")

print("\nModel saved successfully.")


# ==========================================
# Save Preprocessor
# ==========================================

joblib.dump(
    preprocessor,
    "../models/preprocessor.pkl"
)

print("Preprocessor saved successfully.")



print("\n" + "=" * 60)
print("FINAL MODEL COMPARISON")
print("=" * 60)

comparison = pd.DataFrame({
    "Model": ["Dummy Regressor", "ANN"],
    "MAE": [dummy_mae, ann_mae],
    "RMSE": [dummy_rmse, ann_rmse],
    "R2 Score": [dummy_r2, ann_r2]
})

print(comparison)



print("\n" + "=" * 60)
print("BUSINESS INTERPRETATION")
print("=" * 60)

print("1. The ANN predicts house rent more accurately than the Dummy Regressor.")
print("2. Lower MAE means lower average prediction error.")
print("3. Lower RMSE means fewer large prediction errors.")
print("4. Higher R² indicates the ANN explains more variation in house rent.")
print("5. This model can help tenants, landlords, and real-estate companies estimate monthly rent.")
# ==========================================
# Compare Baseline vs ANN
# ==========================================

print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

print(f"Baseline MAE  : {dummy_mae:.2f}")
print(f"ANN MAE       : {ann_mae:.2f}")

print(f"Baseline RMSE : {dummy_rmse:.2f}")
print(f"ANN RMSE      : {ann_rmse:.2f}")

print(f"Baseline R²   : {dummy_r2:.4f}")
print(f"ANN R²        : {ann_r2:.4f}")