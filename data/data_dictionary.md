# Project Management Data Dictionary

Source file: `data/raw/project_management_raw.xlsx`

| Column | Description |
|---|---|
| Project Name | Name of the project or programme |
| Task Name | Individual activity within the project |
| Assigned To | Task owner |
| Priority | Task priority: Low, Medium, High, or Critical |
| Planned Start Date | Scheduled start date |
| Planned End Date | Scheduled completion date |
| Actual End Date | Actual completion date, if available |
| % Complete | Proportion of work completed |
| Planned Budget | Approved task budget |
| Actual Cost | Cost incurred to date |
| Status | Current task status, such as Completed, Delayed, Cancelled, or In Progress |

## Derived fields to create

- `schedule_variance_days`: Actual End Date − Planned End Date
- `budget_variance`: Actual Cost − Planned Budget
- `budget_variance_pct`: Budget Variance / Planned Budget
- `is_delayed`: 1 when status is Delayed or the task finishes after its planned end date
- `is_over_budget`: 1 when Actual Cost exceeds Planned Budget
- `risk_level`: High when a task is critical/high priority and delayed or over budget
- `project_health_score`: A score based on schedule, cost, completion, and risk