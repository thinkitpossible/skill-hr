import { NavLink } from "react-router-dom";
import { ReactNode } from "react";

const navItems = [
  { to: "/dashboard", label: "Business Dashboard" },
  { to: "/employees/dashboard", label: "Employee Dashboard" },
  { to: "/employees", label: "Employee Overview" },
  { to: "/archive", label: "Task Archive" },
  { to: "/templates", label: "Business Templates" },
];

export function MainLayout(props: { children: ReactNode }) {
  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">HR</span>
          <div>
            <strong>Skill HR</strong>
            <p>Dashboard + workforce control</p>
          </div>
        </div>
        <nav className="nav-list">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <p>Built over `.skill-hr` records and `hr_dispatch.py`.</p>
        </div>
      </aside>
      <main className="content">{props.children}</main>
    </div>
  );
}
