import pandas as pd


# Load processed dataset
input_file = "data/processed/telemetry_with_exposure.csv"

df = pd.read_csv(input_file)


print("\n===== FINAL DATASET VALIDATION =====")

# 1. Dataset shape
print("\n===== DATASET SHAPE =====")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# 2. Column names
print("\n===== COLUMNS =====")
print(df.columns.tolist())


# 3. Missing values
print("\n===== MISSING VALUES =====")
print(df.isnull().sum())


# 4. Duplicate records
print("\n===== DUPLICATES =====")
print("Duplicates:", df.duplicated().sum())


# 5. Container count
print("\n===== CONTAINERS =====")
print(df["container_id"].nunique())
print(df["container_id"].unique())


# 6. Commodity count
print("\n===== COMMODITIES =====")
print(df["commodity"].nunique())
print(df["commodity"].unique())


# 7. Risk condition count
print("\n===== RISK CONDITIONS =====")
print(df["risk_condition"].value_counts())


# 8. Risk exposure summary
print("\n===== RISK EXPOSURE SUMMARY =====")

exposure_summary = (
	df.groupby("container_id")["risk_exposure_seconds"]
	.sum()
	.reset_index()
)

print(exposure_summary)


# 9. Sensor ranges
print("\n===== SENSOR RANGES =====")

print(
	"Temperature:",
	df["temperature"].min(),
	"to",
	df["temperature"].max()
)

print(
	"Humidity:",
	df["humidity"].min(),
	"to",
	df["humidity"].max()
)

print(
	"Vibration:",
	df["vibration"].min(),
	"to",
	df["vibration"].max()
)


# 10. Final status
print("\n===== VALIDATION STATUS =====")

if (
	df.shape[0] > 0
	and df.isnull().sum().sum() == 0
	and df.duplicated().sum() == 0
):
	print("Dataset validation PASSED.")
else:
	print("Dataset validation FAILED. Check the data.")
