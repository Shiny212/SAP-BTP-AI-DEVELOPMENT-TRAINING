import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("dataset/loan_default_dataset.csv")

# -------------------------------
# Basic Information
# -------------------------------

print("\nFirst 5 Records")
print(df.head())

print("\nDataset Shape")
print(df.shape)

print("\nColumn Names")
print(df.columns)

print("\nData Types")
print(df.dtypes)

print("\nMissing Values")
print(df.isnull().sum())

print("\nStatistical Summary")
print(df.describe())


plt.figure(figsize=(6,4))
sns.countplot(x="Loan_Default", data=df)
plt.title("Loan Default Distribution")
plt.show()


plt.figure(figsize=(6,4))
sns.histplot(df["Credit_Score"], bins=20, kde=True)
plt.title("Credit Score Distribution")
plt.show()


plt.figure(figsize=(6,4))
sns.boxplot(x="Loan_Default", y="Monthly_Income", data=df)
plt.title("Monthly Income vs Loan Default")
plt.show()


plt.figure(figsize=(6,4))
sns.boxplot(x="Loan_Default", y="Loan_Amount", data=df)
plt.title("Loan Amount vs Loan Default")
plt.show()


plt.figure(figsize=(6,4))
sns.countplot(x="Previous_Default", hue="Loan_Default", data=df)
plt.title("Previous Default vs Current Loan Default")
plt.show()


plt.figure(figsize=(8,4))
sns.countplot(x="Employment_Type", hue="Loan_Default", data=df)
plt.title("Employment Type vs Loan Default")
plt.xticks(rotation=20)
plt.show()


plt.figure(figsize=(10,6))

numeric_df = df.select_dtypes(include="number")

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")
plt.show()


