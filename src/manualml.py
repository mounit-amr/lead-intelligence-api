from sklearn.datasets import load_breast_cancer
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix,average_precision_score, roc_auc_score

data = load_breast_cancer()

df = pd.DataFrame(
    data.data,
    columns=data.feature_names
)

df["Target"] = data.target

X = df.drop("Target", axis=1)
y = df["Target"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# scaler = StandardScaler()

# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# model = LogisticRegression()
# model.fit(X_train_scaled, y_train)

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)

rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

gb_model = GradientBoostingClassifier(
    n_estimators=100,
    random_state=42
)
gb_model.fit(X_train,y_train)
gb_pred = gb_model.predict(X_test)

scores = cross_val_score(
    model,
    X,
    y,
    cv= 5,
    scoring="accuracy"
)

print("\n Cross validation score:")
print(scores)

print("\n Average cv accuracy:", scores.mean())


y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print("confusion matrix:")
print(cm)

y_probability = model.predict_proba(X_test)
print("\n First 10 probabilties:")
print(y_probability[:10])

y_probability_1 = y_probability[:,1]
roc_auc = roc_auc_score(y_test, y_probability_1)

pr_auc = average_precision_score(
    y_test,
    y_probability_1
)
print("\n PR-AUC:", pr_auc)

rf_probability = rf_model.predict_proba(X_test)[:,1]
gb_probability = gb_model.predict_proba(X_test)[:,1]

print("\nROC-AUC:", roc_auc)
print("Logistic Regression:", roc_auc_score(y_test, y_probability_1))
print("Random Forest      :", roc_auc_score(y_test, rf_probability))
print("Gradient Boosting  :", roc_auc_score(y_test, gb_probability))

print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("F1 Score :", f1_score(y_test, y_pred))

print("\nRandom Forest:")
print("Accuracy :", accuracy_score(y_test, rf_pred))
print("Precision:", precision_score(y_test, rf_pred))
print("Recall   :", recall_score(y_test, rf_pred))
print("F1 Score :", f1_score(y_test, rf_pred))

print("\nGradient Boosting:")
print("Accuracy :", accuracy_score(y_test, gb_pred))
print("Precision:", precision_score(y_test, gb_pred))
print("Recall   :", recall_score(y_test, gb_pred))
print("F1 Score :", f1_score(y_test, gb_pred))

class_counts = y.value_counts()
class_percentages = y.value_counts(normalize=True) * 100

print("\nClass counts:")
print(class_counts)

print("\nClass percentages:")
print(class_percentages)