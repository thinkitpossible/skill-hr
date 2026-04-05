import { Outlet } from "react-router-dom";
import { MainLayout } from "./components/MainLayout";

export function App() {
  return (
    <MainLayout>
      <Outlet />
    </MainLayout>
  );
}
