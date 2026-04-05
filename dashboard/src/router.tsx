import { createBrowserRouter, Navigate } from "react-router-dom";
import { App } from "./App";
import { AgentDashboardPage } from "./pages/AgentDashboardPage";
import { BusinessTemplatesPage } from "./pages/BusinessTemplatesPage";
import { EmployeeOverviewPage } from "./pages/EmployeeOverviewPage";
import { TaskArchivePage } from "./pages/TaskArchivePage";
import { TaskDashboardPage } from "./pages/TaskDashboardPage";
import { TaskWorkflowPage } from "./pages/TaskWorkflowPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: "dashboard", element: <TaskDashboardPage /> },
      { path: "employees/dashboard", element: <AgentDashboardPage /> },
      { path: "employees", element: <EmployeeOverviewPage /> },
      { path: "tasks/:taskId", element: <TaskWorkflowPage /> },
      { path: "archive", element: <TaskArchivePage /> },
      { path: "templates", element: <BusinessTemplatesPage /> },
    ],
  },
]);
