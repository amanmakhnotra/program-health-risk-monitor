from pathlib import Path
import sqlite3
import pandas as pd

DATABASE_FILE = Path("data/project_management.db")
QUERY_FILE = Path("sql/analysis_queries.sql")
OUTPUT_DIR = Path("data/processed/sql_results")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

query_names = [
    "portfolio_health_summary",
    "at_risk_projects",
    "owner_workload_risk",
    "project_budget_performance",
    "high_risk_task_exceptions",
]

sql_text = QUERY_FILE.read_text()

queries = [
    query.strip()
    for query in sql_text.split(";")
    if "SELECT" in query.upper()
]

with sqlite3.connect(DATABASE_FILE) as connection:
    for name, query in zip(query_names, queries):
        result = pd.read_sql_query(query, connection)
        output_file = OUTPUT_DIR / f"{name}.csv"
        result.to_csv(output_file, index=False)

        print(f"\n{name}")
        print(result.head(10).to_string(index=False))
        print(f"Saved: {output_file}")

print("\nSQL analysis complete.")