import pandas as pd


INPUT_FILE = "data/processed/telemetry_with_spoilage_score.csv"
OUTPUT_FILE = "data/processed/container_risk_summary.csv"


# Load spoilage score data
df = pd.read_csv(INPUT_FILE)


# Create risk event indicator
df["risk_event"] = df["spoilage_score"] > 0


# Create container-level summary
summary = (
	df.groupby(["container_id", "commodity"])
	.agg(
		total_readings=("container_id", "count"),
		risk_events=("risk_event", "sum"),
		average_spoilage_score=("spoilage_score", "mean"),
		maximum_spoilage_score=("spoilage_score", "max"),
	)
	.reset_index()
)


# Round average score
summary["average_spoilage_score"] = summary["average_spoilage_score"].round(2)


# Assign overall container risk
def get_container_risk(score):
	if score == 0:
		return "LOW"
	elif score <= 40:
		return "MEDIUM"
	else:
		return "HIGH"


summary["overall_risk"] = summary["maximum_spoilage_score"].apply(get_container_risk)


# Display result
print("===== CONTAINER RISK SUMMARY =====")
print()
print(summary.to_string(index=False))


print()
print("===== TOTAL CONTAINERS =====")
print(len(summary))


# Save summary
summary.to_csv(OUTPUT_FILE, index=False)


print()
print("Saved to:")
print(OUTPUT_FILE)
