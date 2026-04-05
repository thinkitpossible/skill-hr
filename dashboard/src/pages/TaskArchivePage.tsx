import { useCallback, useState } from "react";
import { Badge, Card, EmptyState, ErrorBlock, LoadingBlock, PageHeader } from "../components/ui";
import { formatDate, getArchives, Incident, usePollingQuery } from "../lib/api";

export function TaskArchivePage() {
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);
  const archiveQuery = usePollingQuery(useCallback(() => getArchives(), []), 15000);

  if (archiveQuery.loading && !archiveQuery.data) return <LoadingBlock />;
  if (archiveQuery.error) return <ErrorBlock error={archiveQuery.error} />;

  const tasks = archiveQuery.data?.tasks ?? [];
  const incidents = archiveQuery.data?.incidents ?? [];

  return (
    <div className="page">
      <PageHeader
        title="Task Archive"
        description="Review completed and terminated work. Archive records are assembled from terminal task states plus incident markdown."
      />

      <div className="grid two-column">
        <Card title="Archived Tasks">
          {tasks.length ? (
            <div className="stack">
              {tasks.map((task) => (
                <div className="archive-item" key={task.id}>
                  <div>
                    <strong>{task.title}</strong>
                    <p className="muted">
                      {task.id} · {formatDate(task.updated_at)}
                    </p>
                  </div>
                  <Badge>{task.state}</Badge>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No archived tasks" description="Closed and terminated tasks will appear here." />
          )}
        </Card>

        <Card title="Incident Records">
          {incidents.length ? (
            <div className="stack">
              {incidents.map((incident) => (
                <button
                  key={incident.filename}
                  className="list-button"
                  onClick={() => setSelectedIncident(incident)}
                >
                  <strong>{incident.filename}</strong>
                  <span className="muted">{incident.frontmatter.outcome ?? "Unknown outcome"}</span>
                </button>
              ))}
            </div>
          ) : (
            <EmptyState title="No incidents" description="Incident markdown will appear once debriefs are written." />
          )}
        </Card>
      </div>

      {selectedIncident ? (
        <Card title={`Incident Preview · ${selectedIncident.filename}`}>
          <pre className="markdown-preview">{selectedIncident.markdown ?? selectedIncident.body}</pre>
        </Card>
      ) : null}
    </div>
  );
}
