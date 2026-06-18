import { Routes, Route } from "react-router-dom";

import Login from "../pages/Login/Login";
import DepartmentDashboard from "../pages/DepartmentDashboard/DepartmentDashboard";
import AdminDashboard from "../pages/AdminDashboard/AdminDashboard";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/dashboard" element={<DepartmentDashboard />} />
      <Route path="/admin" element={<AdminDashboard />} />
    </Routes>
  );
}

export default AppRoutes;