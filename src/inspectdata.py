from sklearn.datasets import load_breast_cancer
import pandas as pd

data = load_breast_cancer()

df = pd.DataFrame(
    data.data,
    columns=data.feature_names
)

df["Target"] = data.target

print("\n First 5 rows:")
print(df.head())

print("\n Shape:")
print(df.shape)

print("\n columns:")
print(df.columns.to_list())

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\n target distribution")
print(df["Target"].value_counts())

print("\n statistics")
print(df.describe())