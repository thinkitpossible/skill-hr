import { useCallback, useState } from "react";
import { useParams } from "react-router-dom";
import { Badge, Card, EmptyState, ErrorBlock, LoadingBlock, PageHeader } from "../components/ui";
import { formatDate, getIncident, getTask, usePollingQuery } from "../lib/api";

export function TaskWorkflowPage() {
  const { taskId = "" } = useParams();
  const [selectedIncident, setSelectedIncident] = useState<string | null>(null);
  const taskQuery = usePollingQuery(useCallback(() => getTask(taskId), [taskId]), 10000);
  const incidentQuery = usePollingQuery(
    useCallback(() => (selectedIncident ? getIncident(selectedIncident) : Promise.resolve(null)), [selectedIncident]),
    15000,
  );

  if (taskQuery.loading && !taskQuery.data) return <LoadingBlock />;
  if (taskQuery.error) return <ErrorBlock error={taskQuery.error} />;
  if (!taskQuery.data) return <EmptyState title="Task not found" description="The requested workflow could not be loaded." />;

  const task = taskQuery.data;

  return (
    <div className="page">
      <PageHeader
        title={`Task Workflow · ${task.title}`}
        description="Inspect the full handoff timeline, progress snapshots, state notes, and related incidents for one HR task."
      />

      <div className="stats-grid">
        <Card className="compact-card">
          <strong>{task.id}</strong>
          <p className="muted">Current state</p>
          <Badge tone="accent">{task.state}</Badge>
        </Card>
        <Card className="compact-card">
          <strong>{task.current_agent ?? "unassigned"}</strong>
          <p className="muted">Current agent</p>
        </Card>
        <Card className="compact-card">
          <strong>{formatDate(task.created_at)}</strong>
          <p className="muted">Created</p>
        </Card>
        <Card className="compact-card">
          <strong>{formatDate(task.updated_at)}</strong>
          <p className="muted">Updated</p>
        </Card>
      </div>

      <div className="grid two-column">
        <Card title="Flow Log">
          <ul className="timeline">
            {task.flow_log?.length ? (
              task.flow_log.map((entry, index) => (
                <li key={`${entry.ts}-${index}`}>
                  <div className="timeline-marker" />
                  <div>
                    <strong>
                      {entry.from_agent} → {entry.to_agent}
                    </strong>
                    <p className="muted">{formatDate(entry.ts)}</p>
                    <p>{entry.remark}</p>
                  </div>
                </li>
              ))
            ) : (
              <li className="muted">No handoffs recorded yet.</li>
            )}
          </ul>
        </Card>

        <Card title="Progress Log">
          <ul className="timeline">
            {task.progress_log?.length ? (
              task.progress_log.map((entry, index) => (
                <li key={`${entry.ts}-${index}`}>
                  <div className="timeline-marker" />
                  <div>
                    <strong>{entry.current_work}</strong>
                    <p className="muted">{formatDate(entry.ts)}</p>
                    <p>{entry.plan}</p>
                  </div>
                </li>
              ))
            ) : (
              <li className="muted">No progress snapshots recorded yet.</li>
            )}
          </ul>
        </Card>
      </div>

      <div className="grid two-column">
        <Card title="State Notes">
          <ul className="timeline">
            {task.state_notes?.length ? (
              task.state_notes.map((entry, index) => (
                <li key={`${entry.ts}-${index}`}>
                  <div className="timeline-marker" />
                  <div>
                    <strong>{entry.state}</strong>
                    <p className="muted">{formatDate(entry.ts)}</p>
                    <p>{entry.note}</p>
                  </div>
                </li>
              ))
            ) : (
              <li className="muted">No state notes recorded yet.</li>
            )}
          </ul>
        </Card>

        <Card title="Related Incidents">
          {task.related_incidents?.length ? (
            <div className="stack">
              {task.related_incidents.map((incident) => (
                <button
                  key={incident.filename}
                  className="list-button"
                  onClick={() => setSelectedIncident(incident.filename)}
                >
                  <strong>{incident.filename}</strong>
                  <span className="muted">{incident.frontmatter.phase ?? "incident"}</span>
                </button>
              ))}
            </div>
          ) : (
            <EmptyState title="No incidents" description="This task does not have linked incident records yet." />
          )}
        </Card>
      </div>

      {selectedIncident ? (
        <Card title={`Incident · ${selectedIncident}`}>
          {incidentQuery.loading && !incidentQuery.data ? <p>Loading incident...</p> : null}
          {incidentQuery.data ? <pre className="markdown-preview">{incidentQuery.data.markdown}</pre> : null}
        </Card>
      ) : null}
    </div>
  );
}
