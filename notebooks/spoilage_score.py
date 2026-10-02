import pandas as pd


INPUT_FILE = "data/processed/kafka_processed_telemetry.csv"
OUTPUT_FILE = "data/processed/telemetry_with_spoilage_score.csv"


# Load processed Kafka data
df = pd.read_csv(INPUT_FILE)


# Calculate spoilage score
def calculate_spoilage_score(row):
	score = 0

	if row["temperature"] > 30:
		score += 40

	if row["humidity"] > 75:
		score += 40

	return score


df["spoilage_score"] = df.apply(calculate_spoilage_score, axis=1)


# Assign risk level
def get_risk_level(score):
	if score == 0:
		return "LOW"
	elif score <= 40:
		return "MEDIUM"
	else:
		return "HIGH"


df["spoilage_risk_level"] = df["spoilage_score"].apply(get_risk_level)


# Save processed data
df.to_csv(OUTPUT_FILE, index=False)


print("===== SPOILAGE SCORE ANALYSIS =====")
print()

print(
	df[
		[
			"container_id",
			"commodity",
			"temperature",
			"humidity",
			"spoilage_score",
			"spoilage_risk_level",
		]
	]
)

print()
print("===== SCORE SUMMARY =====")
print(df["spoilage_score"].describe())

print()
print("===== RISK LEVEL COUNT =====")
print(df["spoilage_risk_level"].value_counts())

print()
print("Saved to:")
print(OUTPUT_FILE)
