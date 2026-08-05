from pathlib import Path
import sqlite3
import pandas as pd

DATABASE_FILE = Path("data/project_management.db")
OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

exception_query = """
SELECT
    project_name,
    task_name,
    assigned_to,
    priority,
    status,
    pct_complete,
    planned_budget,
    actual_cost,
    budget_variance,
    schedule_variance_days,
    risk_level,
    project_health_score
FROM project_tasks
WHERE risk_level = 'High'
ORDER BY
    project_health_score ASC,
    schedule_variance_days DESC,
    budget_variance DESC;
"""

with sqlite3.connect(DATABASE_FILE) as connection:
    exceptions = pd.read_sql_query(exception_query, connection)

exceptions.insert(0, "risk_rank", range(1, len(exceptions) + 1))

owner_summary = (
    exceptions.groupby("assigned_to", as_index=False)
    .agg(
        high_risk_tasks=("task_name", "count"),
        total_budget_variance=("budget_variance", "sum"),
        average_project_health_score=("project_health_score", "mean"),
    )
    .sort_values(
        ["high_risk_tasks", "average_project_health_score"],
        ascending=[False, True],
    )
)

exceptions.to_csv(
    OUTPUT_DIR / "project_risk_exception_report.csv",
    index=False,
)

owner_summary.to_csv(
    OUTPUT_DIR / "project_risk_summary_by_owner.csv",
    index=False,
)

print(f"Created report for {len(exceptions)} high-risk tasks.")
print("\nHighest-risk owners:")
print(owner_summary.head(10).to_string(index=False))