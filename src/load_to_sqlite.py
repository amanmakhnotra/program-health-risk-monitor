from pathlib import Path
import sqlite3
import pandas as pd

CSV_FILE = Path("data/processed/project_management_clean.csv")
SCHEMA_FILE = Path("sql/create_schema.sql")
DATABASE_FILE = Path("data/project_management.db")

df = pd.read_csv(CSV_FILE)

with sqlite3.connect(DATABASE_FILE) as connection:
    connection.executescript(SCHEMA_FILE.read_text())
    df.to_sql("project_tasks", connection, if_exists="append", index=False)

    task_count = connection.execute(
        "SELECT COUNT(*) FROM project_tasks"
    ).fetchone()[0]

print(f"Loaded {task_count} project tasks into {DATABASE_FILE}.")