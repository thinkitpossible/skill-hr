import { FormEvent, useCallback, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Badge, Card, EmptyState, ErrorBlock, LoadingBlock, PageHeader } from "../components/ui";
import { Template, executeTemplate, getTemplates, usePollingQuery } from "../lib/api";

export function BusinessTemplatesPage() {
  const navigate = useNavigate();
  const templatesQuery = usePollingQuery(useCallback(() => getTemplates(), []), 30000);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [title, setTitle] = useState("");
  const [summary, setSummary] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const templates = templatesQuery.data?.templates ?? [];
  const grouped = useMemo(() => {
    return templates.reduce<Record<string, Template[]>>((acc, template) => {
      acc[template.category] = acc[template.category] ?? [];
      acc[template.category].push(template);
      return acc;
    }, {});
  }, [templates]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!selectedTemplate) return;
    setSubmitting(true);
    try {
      const task = await executeTemplate(selectedTemplate.id, {
        title: title || selectedTemplate.defaults.title,
        summary: summary || selectedTemplate.defaults.summary,
      });
      navigate(`/tasks/${task.id}`);
    } finally {
      setSubmitting(false);
    }
  }

  if (templatesQuery.loading && !templatesQuery.data) return <LoadingBlock />;
  if (templatesQuery.error) return <ErrorBlock error={templatesQuery.error} />;

  return (
    <div className="page">
      <PageHeader
        title="Business Templates"
        description="Seed new HR assignments from reusable business templates, each with keywords, recommended employees, and default task copy."
      />

      <div className="grid two-column">
        <div className="stack">
          {Object.entries(grouped).length ? (
            Object.entries(grouped).map(([category, items]) => (
              <Card key={category} title={category}>
                <div className="stack">
                  {items.map((template) => (
                    <button
                      key={template.id}
                      className={`list-button ${selectedTemplate?.id === template.id ? "selected" : ""}`.trim()}
                      onClick={() => {
                        setSelectedTemplate(template);
                        setTitle(template.defaults.title);
                        setSummary(template.defaults.summary);
                      }}
                    >
                      <div>
                        <strong>{template.name}</strong>
                        <p>{template.description}</p>
                      </div>
                      <Badge tone="subtle">{template.complexity}</Badge>
                    </button>
                  ))}
                </div>
              </Card>
            ))
          ) : (
            <EmptyState title="No templates" description="Add template seed data under `packages/skill-hr/templates/templates.json`." />
          )}
        </div>

        <Card title="Launch Task">
          {selectedTemplate ? (
            <form className="stack" onSubmit={(event) => void handleSubmit(event)}>
              <div className="badge-row">
                {selectedTemplate.keywords.map((keyword) => (
                  <Badge key={keyword} tone="subtle">
                    {keyword}
                  </Badge>
                ))}
              </div>
              <label className="field">
                <span>Task title</span>
                <input value={title} onChange={(event) => setTitle(event.target.value)} />
              </label>
              <label className="field">
                <span>Summary</span>
                <textarea
                  rows={6}
                  value={summary}
                  onChange={(event) => setSummary(event.target.value)}
                />
              </label>
              <p className="muted">
                Recommended employees: {selectedTemplate.recommended_employee_ids.join(", ")}
              </p>
              <button className="button" disabled={submitting} type="submit">
                {submitting ? "Launching..." : "Create task from template"}
              </button>
            </form>
          ) : (
            <EmptyState title="Choose a template" description="Select a template to prefill and create a new HR task." />
          )}
        </Card>
      </div>
    </div>
  );
}
