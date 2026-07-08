import pandas as pd
import numpy as np
import random
import os

# -----------------------------
# Reproducibility
# -----------------------------
random.seed(42)
np.random.seed(42)

# -----------------------------
# Create folders if not exist
# -----------------------------
os.makedirs("../data", exist_ok=True)

# -----------------------------
# Master Data
# -----------------------------
cities = [
    "Bangalore",
    "Chennai",
    "Hyderabad",
    "Mumbai",
    "Delhi",
    "Pune"
]

areas = {
    "Bangalore": [
        "Whitefield",
        "Electronic City",
        "Marathahalli",
        "Indiranagar"
    ],
    "Chennai": [
        "Velachery",
        "T Nagar",
        "OMR",
        "Anna Nagar"
    ],
    "Hyderabad": [
        "Hitech City",
        "Gachibowli",
        "Madhapur",
        "Kukatpally"
    ],
    "Mumbai": [
        "Andheri",
        "Bandra",
        "Powai",
        "Borivali"
    ],
    "Delhi": [
        "Dwarka",
        "Rohini",
        "Saket",
        "Karol Bagh"
    ],
    "Pune": [
        "Hinjewadi",
        "Wakad",
        "Baner",
        "Kharadi"
    ]
}

property_types = [
    "Apartment",
    "Independent House",
    "Villa"
]

furnishing = [
    "Furnished",
    "Semi-Furnished",
    "Unfurnished"
]

parking = [
    "Yes",
    "No"
]

records = []

# -----------------------------
# Create 5000 Records
# -----------------------------
for i in range(1, 5001):

    city = random.choice(cities)

    locality = random.choice(areas[city])

    ptype = random.choice(property_types)

    bhk = random.randint(1, 5)

    size = random.randint(450, 3000)

    bathrooms = random.randint(1, bhk + 1)

    furnish = random.choice(furnishing)

    floor = random.randint(0, 20)

    total_floor = random.randint(floor + 1, 25)

    park = random.choice(parking)

    metro = round(random.uniform(0.2, 10), 2)

    age = random.randint(0, 20)

    # ---------------------------------
    # Generate Realistic Rent
    # ---------------------------------

    rent = (
        size * 22
        + bhk * 1800
        + bathrooms * 900
        - age * 180
        - metro * 650
    )

    if furnish == "Furnished":
        rent += 6000

    elif furnish == "Semi-Furnished":
        rent += 3000

    if park == "Yes":
        rent += 1500

    if city == "Mumbai":
        rent += 18000

    elif city == "Bangalore":
        rent += 8000

    elif city == "Delhi":
        rent += 7000

    elif city == "Hyderabad":
        rent += 5000

    elif city == "Pune":
        rent += 4000

    elif city == "Chennai":
        rent += 4500

    rent += random.randint(-3000, 3000)

    rent = max(8000, int(rent))

    records.append([
        f"P{i:05}",
        city,
        locality,
        ptype,
        bhk,
        size,
        bathrooms,
        furnish,
        floor,
        total_floor,
        park,
        metro,
        age,
        rent
    ])

# -----------------------------
# Create DataFrame
# -----------------------------

columns = [
    "Property_ID",
    "City",
    "Area_Locality",
    "Property_Type",
    "BHK",
    "Size_sqft",
    "Bathroom_Count",
    "Furnishing_Status",
    "Floor_Number",
    "Total_Floors",
    "Parking_Available",
    "Distance_to_Metro_km",
    "Property_Age_Years",
    "Monthly_Rent"
]

df = pd.DataFrame(records, columns=columns)

# -----------------------------
# Introduce Missing Values
# -----------------------------

for col in [
    "Size_sqft",
    "Bathroom_Count",
    "Furnishing_Status"
]:

    idx = np.random.choice(df.index, 80)

    df.loc[idx, col] = np.nan

# -----------------------------
# Save CSV
# -----------------------------

df.to_csv("../data/house_rent.csv", index=False)

print("=" * 50)
print("House Rent Dataset Created Successfully")
print("=" * 50)

print()

print("Shape :", df.shape)

print()

print(df.head())

print()

print(df.isnull().sum())