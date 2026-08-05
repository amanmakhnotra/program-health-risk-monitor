-- 1. Portfolio health summary
SELECT
    COUNT(DISTINCT project_name) AS total_projects,
    COUNT(*) AS total_tasks,
    ROUND(100.0 * AVG(pct_complete), 1) AS average_completion_pct,
    SUM(is_delayed) AS delayed_tasks,
    SUM(is_over_budget) AS over_budget_tasks,
    SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) AS high_risk_tasks,
    ROUND(AVG(project_health_score), 1) AS average_portfolio_health_score
FROM project_tasks;


-- 2. Projects needing the most attention
SELECT
    project_name,
    project_health_score,
    health_status,
    delayed_tasks,
    over_budget_tasks,
    average_completion_pct,
    total_budget_variance
FROM project_health_summary
ORDER BY project_health_score ASC;


-- 3. Owner workload and risk
SELECT
    assigned_to,
    COUNT(*) AS total_tasks,
    SUM(is_delayed) AS delayed_tasks,
    SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) AS high_risk_tasks,
    ROUND(100.0 * AVG(pct_complete), 1) AS average_completion_pct
FROM project_tasks
GROUP BY assigned_to
ORDER BY high_risk_tasks DESC, delayed_tasks DESC;


-- 4. Project budget performance
SELECT
    project_name,
    ROUND(SUM(planned_budget), 2) AS planned_budget,
    ROUND(SUM(actual_cost), 2) AS actual_cost,
    ROUND(SUM(budget_variance), 2) AS budget_variance,
    SUM(is_over_budget) AS over_budget_tasks
FROM project_tasks
GROUP BY project_name
ORDER BY budget_variance DESC;


-- 5. High-risk task exceptions
SELECT
    project_name,
    task_name,
    assigned_to,
    priority,
    status,
    pct_complete,
    planned_end_date,
    actual_end_date,
    budget_variance,
    schedule_variance_days,
    risk_level,
    project_health_score
FROM project_tasks
WHERE risk_level = 'High'
ORDER BY project_health_score ASC, budget_variance DESC;