import pandas as pd

# Load dataset
df = pd.read_csv("dataset/disasterIND.csv")

# Keep only important columns
df = df[[
    "Location",
    "Disaster Type",
    "Disaster Subtype",
    "Start Year",
    "Total Deaths",
    "Total Damage ('000 US$)"
]]

# Remove rows with missing location
df = df.dropna(subset=["Location"])

# Save cleaned file
df.to_csv("dataset/clean_disaster_data.csv", index=False)

print("✅ Data cleaned successfully")
