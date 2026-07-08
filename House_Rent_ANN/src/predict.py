import os

# Hide TensorFlow C++ logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import joblib

import tensorflow as tf

# Hide TensorFlow Python logs
tf.get_logger().setLevel("ERROR")

from tensorflow.keras.models import load_model

# ==========================================
# Load Saved Model
# ==========================================

model = load_model("../models/house_rent_ann.keras")

# ==========================================
# Load Preprocessor
# ==========================================

preprocessor = joblib.load("../models/preprocessor.pkl")

# ==========================================
# New Property Details
# ==========================================

new_property = pd.DataFrame({

    "City": ["Bangalore"],

    "Area_Locality": ["Whitefield"],

    "Property_Type": ["Apartment"],

    "BHK": [2],

    "Size_sqft": [1050],

    "Bathroom_Count": [2],

    "Furnishing_Status": ["Semi-Furnished"],

    "Floor_Number": [5],

    "Total_Floors": [12],

    "Parking_Available": ["Yes"],

    "Distance_to_Metro_km": [1.5],

    "Property_Age_Years": [4]

})

# ==========================================
# Apply Preprocessing
# ==========================================

new_property_processed = preprocessor.transform(new_property)

# ==========================================
# Predict Rent
# ==========================================

predicted_rent = model.predict(new_property_processed)

print("\n" + "=" * 60)
print("HOUSE RENT PREDICTION")
print("=" * 60)

print(f"Predicted Monthly Rent : ₹{predicted_rent[0][0]:,.2f}")