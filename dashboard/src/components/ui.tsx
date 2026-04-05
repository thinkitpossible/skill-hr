import { ReactNode } from "react";

export function PageHeader(props: {
  title: string;
  description: string;
  actions?: ReactNode;
}) {
  return (
    <div className="page-header">
      <div>
        <h1>{props.title}</h1>
        <p>{props.description}</p>
      </div>
      {props.actions ? <div className="header-actions">{props.actions}</div> : null}
    </div>
  );
}

export function StatCard(props: { label: string; value: string | number; tone?: string }) {
  return (
    <div className={`card stat-card ${props.tone ?? ""}`.trim()}>
      <span className="stat-label">{props.label}</span>
      <strong className="stat-value">{props.value}</strong>
    </div>
  );
}

export function Card(props: { title?: string; children: ReactNode; className?: string }) {
  return (
    <section className={`card ${props.className ?? ""}`.trim()}>
      {props.title ? <h2 className="card-title">{props.title}</h2> : null}
      {props.children}
    </section>
  );
}

export function Badge(props: { children: ReactNode; tone?: string }) {
  return (
    <span className={`badge ${props.tone ?? "default"}`.trim()}>
      {props.children}
    </span>
  );
}

export function EmptyState(props: { title: string; description: string }) {
  return (
    <div className="empty-state">
      <h3>{props.title}</h3>
      <p>{props.description}</p>
    </div>
  );
}

export function LoadingBlock() {
  return <div className="card loading">Loading dashboard data...</div>;
}

export function ErrorBlock(props: { error: string }) {
  return <div className="card error">{props.error}</div>;
}
