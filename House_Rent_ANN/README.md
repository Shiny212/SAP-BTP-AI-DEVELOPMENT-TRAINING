# House Rent Prediction Using Artificial Neural Network (ANN)

## Project Overview

This project predicts the monthly rent of a house using an Artificial Neural Network (ANN). The model is trained on a synthetic dataset of 5000 records.

## Objective

Predict the monthly rent of a property based on:

- City
- Area
- Property Type
- BHK
- Property Size
- Bathrooms
- Furnishing Status
- Floor Number
- Total Floors
- Parking Availability
- Distance to Metro
- Property Age

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- TensorFlow/Keras
- Joblib

---

## Project Structure

```
House_Rent_ANN/
│
├── data/
│   └── house_rent.csv
│
├── models/
│   ├── house_rent_ann.keras
│   └── preprocessor.pkl
│
├── plots/
│
├── src/
│   ├── create_dataset.py
│   ├── train_ann.py
│   └── predict.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Machine Learning Workflow

1. Dataset Creation
2. Exploratory Data Analysis (EDA)
3. Missing Value Handling
4. Feature Engineering
5. Data Preprocessing
6. Train-Test Split
7. Dummy Regressor (Baseline)
8. Artificial Neural Network
9. Model Evaluation
10. Prediction

---

## ANN Architecture

- Input Layer
- Dense (128, ReLU)
- Dropout (0.3)
- Dense (64, ReLU)
- Dropout (0.2)
- Dense (32, ReLU)
- Output Layer (1 Neuron)

---

## Evaluation Metrics

- MAE
- RMSE
- R² Score

---

## Future Improvements

- Hyperparameter tuning
- Cross-validation
- Deployment using Streamlit
- Cloud deployment on SAP BTP

---

## Author

Shiny Belsiya
