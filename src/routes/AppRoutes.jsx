import { Routes, Route } from "react-router-dom";

import Login from "../pages/Login/Login";
import DepartmentDashboard from "../pages/DepartmentDashboard/DepartmentDashboard";
import ProtectedRoute from "./ProtectedRoute";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DepartmentDashboard />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

export default AppRoutes;