import { useCallback, useMemo, useState } from "react";
import { Badge, Card, EmptyState, ErrorBlock, LoadingBlock, PageHeader } from "../components/ui";
import { Employee, formatDate, getEmployees, updateEmployeeStatus, usePollingQuery } from "../lib/api";

export function EmployeeOverviewPage() {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<Employee | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const employeesQuery = usePollingQuery(useCallback(() => getEmployees(), [refreshKey]), 10000);

  const employees = employeesQuery.data?.employees ?? [];
  const filtered = useMemo(() => {
    const lowered = query.toLowerCase();
    return employees.filter((employee) => {
      const haystack = [
        employee.id,
        employee.name,
        employee.status,
        employee.host,
        employee.primary_skill,
        ...employee.skills,
      ]
        .join(" ")
        .toLowerCase();
      return haystack.includes(lowered);
    });
  }, [employees, query]);

  async function setStatus(employeeId: string, status: string) {
    const updated = await updateEmployeeStatus(employeeId, status, `Updated from overview to ${status}`);
    setSelected(updated);
    setRefreshKey((value) => value + 1);
  }

  if (employeesQuery.loading && !employeesQuery.data) return <LoadingBlock />;
  if (employeesQuery.error) return <ErrorBlock error={employeesQuery.error} />;

  return (
    <div className="page">
      <PageHeader
        title="Employee Overview"
        description="Browse the employee database, inspect multi-skill bundles, and manage employee status without touching the registry by hand."
        actions={
          <input
            className="search-input"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search employees, skills, hosts..."
          />
        }
      />

      <Card>
        {filtered.length ? (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Status</th>
                  <th>Host</th>
                  <th>Skills</th>
                  <th>Success rate</th>
                  <th>Last used</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((employee) => (
                  <tr key={employee.id} onClick={() => setSelected(employee)}>
                    <td>
                      <strong>{employee.name}</strong>
                      <div className="muted">{employee.id}</div>
                    </td>
                    <td>
                      <Badge>{employee.status}</Badge>
                    </td>
                    <td>{employee.host}</td>
                    <td>
                      <div className="badge-row">
                        {employee.skills.map((skill) => (
                          <Badge key={skill} tone="subtle">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </td>
                    <td>{employee.success_rate}%</td>
                    <td>{formatDate(employee.last_used_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyState title="No employees found" description="Try a different filter or seed the registry with employee records." />
        )}
      </Card>

      {selected ? (
        <Card title={`Employee Detail · ${selected.name}`}>
          <div className="detail-grid">
            <div>
              <p>
                <strong>Role:</strong> {selected.role_title ?? "N/A"}
              </p>
              <p>
                <strong>Primary skill:</strong> {selected.primary_skill}
              </p>
              <p>
                <strong>Added:</strong> {formatDate(selected.added_at)}
              </p>
              <p>
                <strong>Notes:</strong> {selected.notes ?? "No notes"}
              </p>
            </div>
            <div>
              <p>
                <strong>Total tasks:</strong> {selected.performance.tasks_total}
              </p>
              <p>
                <strong>Successful tasks:</strong> {selected.performance.tasks_success}
              </p>
              <p>
                <strong>Failed tasks:</strong> {selected.performance.tasks_fail}
              </p>
            </div>
          </div>

          <div className="toolbar-row">
            <button className="button secondary" onClick={() => void setStatus(selected.id, "active")}>
              Mark active
            </button>
            <button className="button secondary" onClick={() => void setStatus(selected.id, "on_probation")}>
              Put on probation
            </button>
            <button className="button secondary" onClick={() => void setStatus(selected.id, "frozen")}>
              Freeze
            </button>
            <button className="button danger" onClick={() => void setStatus(selected.id, "terminated")}>
              Terminate
            </button>
          </div>

          <div className="grid two-column">
            <Card title="Training History" className="nested-card">
              <ul className="timeline">
                {selected.training_history.length ? (
                  selected.training_history.map((entry, index) => (
                    <li key={`${entry.ts}-${index}`}>
                      <div className="timeline-marker" />
                      <div>
                        <strong>{entry.action}</strong>
                        <p className="muted">{formatDate(entry.ts)}</p>
                        <p>{entry.notes ?? "No notes provided."}</p>
                      </div>
                    </li>
                  ))
                ) : (
                  <li className="muted">No training events yet.</li>
                )}
              </ul>
            </Card>

            <Card title="Related Incidents" className="nested-card">
              <ul className="compact-list">
                {selected.related_incidents.length ? (
                  selected.related_incidents.map((incident) => (
                    <li key={incident.filename}>{incident.filename}</li>
                  ))
                ) : (
                  <li className="muted">No incidents linked yet.</li>
                )}
              </ul>
            </Card>
          </div>
        </Card>
      ) : null}
    </div>
  );
}
