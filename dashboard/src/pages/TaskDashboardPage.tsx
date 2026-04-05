import { useCallback, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { Badge, Card, EmptyState, ErrorBlock, LoadingBlock, PageHeader, StatCard } from "../components/ui";
import { Task, formatDate, getStats, getTasks, updateTaskState, usePollingQuery } from "../lib/api";

const KANBAN_STATES = [
  "Intake",
  "Designing",
  "Training",
  "TrainingReview",
  "JDReady",
  "Matching",
  "Matched",
  "Recruiting",
  "Vetting",
  "Delegated",
  "InProgress",
  "Debrief",
  "Closed",
];

/** Default "Advance" step — must match `hr_dispatch.py` `_VALID_TRANSITIONS` happy paths. */
const DEFAULT_ADVANCE: Record<string, string> = {
  Intake: "JDReady",
  Designing: "Training",
  Training: "TrainingReview",
  TrainingReview: "Matching",
  JDReady: "Matching",
  Matching: "Matched",
  Matched: "Delegated",
  Recruiting: "Vetting",
  Vetting: "Matched",
  Delegated: "InProgress",
  InProgress: "Debrief",
  Debrief: "Closed",
};

export function TaskDashboardPage() {
  const [refreshKey, setRefreshKey] = useState(0);
  const tasksLoader = useCallback(() => getTasks(), [refreshKey]);
  const statsLoader = useCallback(() => getStats(), [refreshKey]);
  const { data, loading, error } = usePollingQuery(tasksLoader, 10000);
  const statsQuery = usePollingQuery(statsLoader, 10000);

  const tasksByState = useMemo(() => {
    const grouped: Record<string, Task[]> = {};
    for (const state of KANBAN_STATES) grouped[state] = [];
    for (const task of data?.tasks ?? []) {
      if (grouped[task.state]) grouped[task.state].push(task);
    }
    return grouped;
  }, [data]);

  async function handleAdvance(task: Task) {
    const nextState = DEFAULT_ADVANCE[task.state];
    if (!nextState) return;
    await updateTaskState(task.id, nextState, `Advanced from dashboard to ${nextState}`);
    setRefreshKey((value) => value + 1);
  }

  if (loading && !data) return <LoadingBlock />;
  if (error) return <ErrorBlock error={error} />;

  return (
    <div className="page">
      <PageHeader
        title="Business Dashboard"
        description="Track active HR tasks from intake through debrief. This view mirrors `hr_tasks.json` and only mutates state through the local bridge."
      />

      <div className="stats-grid">
        <StatCard label="Active tasks" value={statsQuery.data?.task_total ?? 0} />
        <StatCard label="Employees" value={statsQuery.data?.employee_total ?? 0} />
        <StatCard label="HR agents" value={statsQuery.data?.hr_agent_total ?? 0} />
        <StatCard label="Incidents" value={statsQuery.data?.incident_total ?? 0} />
      </div>

      <div className="kanban-board">
        {KANBAN_STATES.map((state) => (
          <div className="kanban-column" key={state}>
            <div className="kanban-column-header">
              <h2>{state}</h2>
              <Badge>{tasksByState[state]?.length ?? 0}</Badge>
            </div>
            <div className="kanban-stack">
              {tasksByState[state]?.length ? (
                tasksByState[state].map((task) => (
                  <Card key={task.id} className="task-card">
                    <div className="task-card-top">
                      <Badge tone="accent">{task.current_agent ?? "unassigned"}</Badge>
                      <span className="muted">{task.id}</span>
                    </div>
                    <h3>{task.title}</h3>
                    <p className="muted">Updated {formatDate(task.updated_at)}</p>
                    <div className="task-card-actions">
                      <Link to={`/tasks/${task.id}`} className="button secondary">
                        View workflow
                      </Link>
                      {DEFAULT_ADVANCE[task.state] ? (
                        <button className="button" onClick={() => void handleAdvance(task)}>
                          Advance
                        </button>
                      ) : null}
                    </div>
                  </Card>
                ))
              ) : (
                <EmptyState title="No tasks" description={`No active tasks are currently in ${state}.`} />
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
