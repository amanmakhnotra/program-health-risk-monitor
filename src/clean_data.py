from pathlib import Path
import json
import pandas as pd

RAW_FILE = Path("data/raw/project_management_raw.xlsx")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_excel(RAW_FILE)

df.columns = [
    "project_name",
    "task_name",
    "assigned_to",
    "priority",
    "planned_start_date",
    "planned_end_date",
    "actual_end_date",
    "pct_complete",
    "planned_budget",
    "actual_cost",
    "status",
]

for column in [
    "planned_start_date",
    "planned_end_date",
    "actual_end_date",
]:
    df[column] = pd.to_datetime(df[column], errors="coerce")

for column in ["project_name", "task_name", "assigned_to", "priority", "status"]:
    df[column] = df[column].astype(str).str.strip()

df["schedule_variance_days"] = (
    df["actual_end_date"] - df["planned_end_date"]
).dt.days

df["budget_variance"] = df["actual_cost"] - df["planned_budget"]
df["budget_variance_pct"] = (
    df["budget_variance"] / df["planned_budget"]
).fillna(0)

df["is_delayed"] = (
    (df["status"].str.lower() == "delayed")
    | (df["schedule_variance_days"] > 0)
).astype(int)

df["is_over_budget"] = (
    df["actual_cost"] > df["planned_budget"]
).astype(int)

df["risk_level"] = "Low"
df.loc[
    (df["is_delayed"] == 1) | (df["is_over_budget"] == 1),
    "risk_level",
] = "Medium"
df.loc[
    df["priority"].str.lower().isin(["high", "critical"])
    & ((df["is_delayed"] == 1) | (df["is_over_budget"] == 1)),
    "risk_level",
] = "High"

df["project_health_score"] = 100
df.loc[df["is_delayed"] == 1, "project_health_score"] -= 40
df.loc[df["is_over_budget"] == 1, "project_health_score"] -= 30
df.loc[df["status"].str.lower() == "cancelled", "project_health_score"] -= 50
df.loc[
    (df["priority"].str.lower().isin(["high", "critical"]))
    & (df["pct_complete"] < 0.5),
    "project_health_score",
] -= 15

df["project_health_score"] = df["project_health_score"].clip(0, 100)

quality_report = {
    "total_rows": len(df),
    "missing_values": df.isna().sum().to_dict(),
    "invalid_budget_rows": int(
        ((df["planned_budget"] < 0) | (df["actual_cost"] < 0)).sum()
    ),
    "invalid_completion_rows": int(
        ((df["pct_complete"] < 0) | (df["pct_complete"] > 1)).sum()
    ),
    "invalid_schedule_rows": int(
        (df["planned_end_date"] < df["planned_start_date"]).sum()
    ),
}

df.to_csv(OUTPUT_DIR / "project_management_clean.csv", index=False)

with open(OUTPUT_DIR / "data_quality_report.json", "w") as file:
    json.dump(quality_report, file, indent=2, default=str)

print("Cleaning complete.")
print(json.dumps(quality_report, indent=2))