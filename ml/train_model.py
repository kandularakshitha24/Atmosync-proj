import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os


# -----------------------------------------
# 1. Load dataset
# -----------------------------------------

DATA_PATH = "data/processed/telemetry_with_spoilage_score.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully.")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# -----------------------------------------
# 2. Select features and target
# -----------------------------------------

features = [
	"temperature",
	"humidity",
	"vibration"
]

target = "spoilage_risk_level"

X = df[features]
y = df[target]


# -----------------------------------------
# 3. Encode target labels
# -----------------------------------------

label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)

print("\nRisk classes:")
for label, encoded_value in zip(
	label_encoder.classes_,
	label_encoder.transform(label_encoder.classes_)
):
	print(f"{label} -> {encoded_value}")


# -----------------------------------------
# 4. Train-test split
# -----------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
	X,
	y_encoded,
	test_size=0.20,
	random_state=42,
	stratify=y_encoded
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------------------
# 5. Train Random Forest model
# -----------------------------------------

model = RandomForestClassifier(
	n_estimators=100,
	random_state=42
)

model.fit(X_train, y_train)


# -----------------------------------------
# 6. Evaluate model
# -----------------------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(
	classification_report(
		y_test,
		y_pred,
		target_names=label_encoder.classes_,
		zero_division=0
	)
)


# -----------------------------------------
# 7. Save model
# -----------------------------------------

os.makedirs("ml/models", exist_ok=True)

joblib.dump(
	model,
	"ml/models/spoilage_risk_model.pkl"
)

joblib.dump(
	label_encoder,
	"ml/models/risk_label_encoder.pkl"
)

print("\nModel saved successfully.")

print("Model:")
print("ml/models/spoilage_risk_model.pkl")

print("Label encoder:")
print("ml/models/risk_label_encoder.pkl")
