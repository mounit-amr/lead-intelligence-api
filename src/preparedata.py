from sklearn.datasets import load_breast_cancer
import pandas as pd

data = load_breast_cancer()

df = pd.DataFrame(
    data.data,
    columns=data.feature_names
)

df["Target"] = data.target

X = df.drop("Target", axis=1)
y = df["Target"]

print("X shape:", X.shape)
print("y shape:", y.shape)

print("\n X")
print(X.head())

print("\n y")
print(y.head())

print("\nTarget distribution:")
print(y.value_counts())