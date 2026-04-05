import { useCallback } from "react";
import { Badge, Card, ErrorBlock, LoadingBlock, PageHeader, StatCard } from "../components/ui";
import { getEmployees, getHrAgents, usePollingQuery } from "../lib/api";

export function AgentDashboardPage() {
  const agentsQuery = usePollingQuery(useCallback(() => getHrAgents(), []), 10000);
  const employeesQuery = usePollingQuery(useCallback(() => getEmployees(), []), 10000);

  if (agentsQuery.loading && !agentsQuery.data) return <LoadingBlock />;
  if (agentsQuery.error) return <ErrorBlock error={agentsQuery.error} />;

  const employees = employeesQuery.data?.employees ?? [];
  const hostCounts = employees.reduce<Record<string, number>>((acc, employee) => {
    acc[employee.host] = (acc[employee.host] ?? 0) + 1;
    return acc;
  }, {});

  return (
    <div className="page">
      <PageHeader
        title="Employee Dashboard"
        description="Observe the HR department and the active workforce. The top grid shows the HR operating team, while the summary cards track deployed employees by host and readiness."
      />

      <div className="stats-grid">
        <StatCard label="Active employees" value={employees.length} />
        <StatCard label="Claude Code" value={hostCounts["claude-code"] ?? 0} />
        <StatCard label="OpenClaw" value={hostCounts["openclaw"] ?? 0} />
        <StatCard label="On probation" value={employees.filter((item) => item.status === "on_probation").length} />
      </div>

      <Card title="HR Department">
        <div className="grid two-column">
          {agentsQuery.data?.agents.map((agent) => (
            <div key={agent.id} className="agent-card">
              <div className="agent-card-top">
                <div>
                  <h3>{agent.id}</h3>
                  <p className="muted">{agent.role}</p>
                </div>
                <Badge tone={agent.health === "busy" ? "accent" : "default"}>{agent.health}</Badge>
              </div>
              <p>{agent.active_task_count} task(s) currently assigned.</p>
              <ul className="compact-list">
                {agent.current_tasks.length ? (
                  agent.current_tasks.map((task) => (
                    <li key={task.id}>
                      <strong>{task.title}</strong> <span className="muted">({task.state})</span>
                    </li>
                  ))
                ) : (
                  <li className="muted">No current assignments.</li>
                )}
              </ul>
            </div>
          ))}
        </div>
      </Card>

      <Card title="Workforce Snapshot">
        <div className="grid two-column">
          {employees.map((employee) => (
            <div className="employee-mini-card" key={employee.id}>
              <div className="agent-card-top">
                <div>
                  <h3>{employee.name}</h3>
                  <p className="muted">{employee.role_title ?? employee.primary_skill}</p>
                </div>
                <Badge>{employee.status}</Badge>
              </div>
              <p className="muted">
                Host: {employee.host} · Success rate: {employee.success_rate}%
              </p>
              <div className="badge-row">
                {employee.skills.map((skill) => (
                  <Badge key={skill} tone="subtle">
                    {skill}
                  </Badge>
                ))}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
