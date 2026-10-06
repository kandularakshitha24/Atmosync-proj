import pandas as pd
import joblib


# -----------------------------------------
# 1. Load trained model
# -----------------------------------------

MODEL_PATH = "ml/models/spoilage_risk_model.pkl"
ENCODER_PATH = "ml/models/risk_label_encoder.pkl"

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)


# -----------------------------------------
# 2. Create sample telemetry input
# -----------------------------------------

temperature = 34.0
humidity = 82.0
vibration = 0.30

input_data = pd.DataFrame(
	[[temperature, humidity, vibration]],
	columns=["temperature", "humidity", "vibration"],
)


# -----------------------------------------
# 3. Predict risk
# -----------------------------------------

prediction = model.predict(input_data)
predicted_risk = label_encoder.inverse_transform(prediction)[0]


# -----------------------------------------
# 4. Display result
# -----------------------------------------

print("AtmoSync ML Risk Prediction")
print("----------------------------")
print(f"Temperature : {temperature} °C")
print(f"Humidity    : {humidity} %")
print(f"Vibration   : {vibration}")
print()
print(f"Predicted Spoilage Risk: {predicted_risk}")
