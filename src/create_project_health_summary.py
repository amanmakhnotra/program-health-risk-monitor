from pathlib import Path
import sqlite3
import pandas as pd

DATABASE_FILE = Path("data/project_management.db")
SQL_FILE = Path("sql/create_project_health_summary.sql")
OUTPUT_FILE = Path("data/processed/project_health_summary.csv")

with sqlite3.connect(DATABASE_FILE) as connection:
    connection.executescript(SQL_FILE.read_text())

    summary = pd.read_sql_query(
        """
        SELECT *
        FROM project_health_summary
        ORDER BY project_health_score ASC
        """,
        connection,
    )

summary.to_csv(OUTPUT_FILE, index=False)

print(summary.head(10).to_string(index=False))
print(f"\nSaved: {OUTPUT_FILE}")
