import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Load trained model
model = joblib.load("models/best_random_forest.pkl")

# Get feature names
feature_names = model.named_steps["preprocessor"].get_feature_names_out()

# Get importance values
importance = model.named_steps["classifier"].feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print(importance_df.head(15))

# Plot
plt.figure(figsize=(10,6))

plt.barh(
    importance_df["Feature"][:10],
    importance_df["Importance"][:10]
)

plt.title("Top 10 Feature Importance")

plt.xlabel("Importance")

plt.gca().invert_yaxis()

plt.show()