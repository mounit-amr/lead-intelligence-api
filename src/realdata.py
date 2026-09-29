import pandas as pd

df = pd.read_csv("data/leads.csv")

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 row:")
print(df.head())

print("Missing values:")
print(df.isnull().sum())

print("\nTarget distribution:")
print(df["converted"].value_counts())

