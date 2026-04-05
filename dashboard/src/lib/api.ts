import { useEffect, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8787";

export interface Task {
  id: string;
  title: string;
  state: string;
  created_at?: string;
  updated_at?: string;
  current_agent?: string;
  flow_log?: Array<{
    ts: string;
    from_agent: string;
    to_agent: string;
    remark: string;
  }>;
  progress_log?: Array<{
    ts: string;
    current_work: string;
    plan: string;
  }>;
  state_notes?: Array<{
    ts: string;
    state: string;
    note: string;
  }>;
  related_incidents?: Array<{
    filename: string;
    frontmatter: Record<string, string>;
  }>;
}

export interface HrAgent {
  id: string;
  name: string;
  role: string;
  active_task_count: number;
  current_tasks: Array<{ id: string; title: string; state: string }>;
  health: string;
}

export interface Employee {
  id: string;
  name: string;
  status: string;
  skills: string[];
  primary_skill: string;
  host: string;
  created_by: string;
  role_title?: string;
  added_at?: string;
  last_used_at?: string;
  notes?: string;
  success_rate: number;
  performance: {
    tasks_total: number;
    tasks_success: number;
    tasks_fail: number;
  };
  training_history: Array<{
    ts: string;
    action: string;
    notes?: string;
  }>;
  skill_details: Array<{
    id: string;
    name: string;
    description?: string;
    status: string;
  }>;
  related_incidents: Array<{
    filename: string;
    frontmatter: Record<string, string>;
  }>;
}

export interface Template {
  id: string;
  name: string;
  category: string;
  description: string;
  complexity: string;
  keywords: string[];
  recommended_employee_ids: string[];
  defaults: {
    title: string;
    summary: string;
  };
}

export interface Incident {
  filename: string;
  frontmatter: Record<string, string>;
  body?: string;
  markdown?: string;
}

export interface StatsResponse {
  task_counts: Record<string, number>;
  task_total: number;
  employee_total: number;
  hr_agent_total: number;
  incident_total: number;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }
  return (await response.json()) as T;
}

export async function getTasks(state?: string) {
  const suffix = state ? `?state=${encodeURIComponent(state)}` : "";
  return request<{ tasks: Task[] }>(`/api/tasks${suffix}`);
}

export async function getTask(taskId: string) {
  return request<Task>(`/api/tasks/${taskId}`);
}

export async function getArchives() {
  return request<{ tasks: Task[]; incidents: Incident[] }>("/api/archives");
}

export async function getHrAgents() {
  return request<{ agents: HrAgent[] }>("/api/agents");
}

export async function getEmployees() {
  return request<{ employees: Employee[] }>("/api/employees");
}

export async function getEmployee(employeeId: string) {
  return request<Employee>(`/api/employees/${employeeId}`);
}

export async function updateEmployeeStatus(employeeId: string, status: string, note?: string) {
  return request<Employee>(`/api/employees/${employeeId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status, note }),
  });
}

export async function getTemplates() {
  return request<{ templates: Template[] }>("/api/templates");
}

export async function executeTemplate(templateId: string, payload: { title: string; summary: string }) {
  return request<Task>(`/api/templates/${templateId}/execute`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function createTask(payload: { title: string; summary: string }) {
  return request<Task>("/api/tasks", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateTaskState(taskId: string, newState: string, note?: string) {
  return request<Task>(`/api/tasks/${taskId}/state`, {
    method: "PATCH",
    body: JSON.stringify({ new_state: newState, note }),
  });
}

export async function getIncidents() {
  return request<{ incidents: Incident[] }>("/api/incidents");
}

export async function getIncident(filename: string) {
  return request<Incident>(`/api/incidents/${filename}`);
}

export async function getStats() {
  return request<StatsResponse>("/api/stats");
}

export function usePollingQuery<T>(loader: () => Promise<T>, intervalMs = 15000) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    let timer: number | undefined;

    async function run() {
      try {
        const result = await loader();
        if (!active) return;
        setData(result);
        setError(null);
      } catch (err) {
        if (!active) return;
        setError(err instanceof Error ? err.message : String(err));
      } finally {
        if (active) setLoading(false);
        if (active) {
          timer = window.setTimeout(run, intervalMs);
        }
      }
    }

    run();
    return () => {
      active = false;
      if (timer) window.clearTimeout(timer);
    };
  }, [intervalMs, loader]);

  return { data, loading, error };
}

export function formatDate(value?: string) {
  if (!value) return "N/A";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}
