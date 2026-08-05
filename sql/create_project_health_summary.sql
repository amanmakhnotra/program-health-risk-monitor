DROP VIEW IF EXISTS project_health_summary;

CREATE VIEW project_health_summary AS
SELECT
    project_name,
    COUNT(*) AS total_tasks,
    ROUND(100.0 * AVG(pct_complete), 1) AS average_completion_pct,
    SUM(is_delayed) AS delayed_tasks,
    SUM(is_over_budget) AS over_budget_tasks,
    ROUND(SUM(planned_budget), 2) AS total_planned_budget,
    ROUND(SUM(actual_cost), 2) AS total_actual_cost,
    ROUND(SUM(budget_variance), 2) AS total_budget_variance,
    ROUND(AVG(project_health_score), 1) AS project_health_score,
    CASE
        WHEN AVG(project_health_score) >= 80 THEN 'Green'
        WHEN AVG(project_health_score) >= 60 THEN 'Amber'
        ELSE 'Red'
    END AS health_status
FROM project_tasks
GROUP BY project_name;