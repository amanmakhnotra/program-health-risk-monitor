DROP TABLE IF EXISTS project_tasks;

CREATE TABLE project_tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT,
    task_name TEXT,
    assigned_to TEXT,
    priority TEXT,
    planned_start_date TEXT,
    planned_end_date TEXT,
    actual_end_date TEXT,
    pct_complete REAL,
    planned_budget REAL,
    actual_cost REAL,
    status TEXT,
    schedule_variance_days INTEGER,
    budget_variance REAL,
    budget_variance_pct REAL,
    is_delayed INTEGER,
    is_over_budget INTEGER,
    risk_level TEXT,
    project_health_score INTEGER
);

CREATE INDEX idx_project_tasks_project ON project_tasks(project_name);
CREATE INDEX idx_project_tasks_owner ON project_tasks(assigned_to);
CREATE INDEX idx_project_tasks_status ON project_tasks(status);
CREATE INDEX idx_project_tasks_risk ON project_tasks(risk_level);