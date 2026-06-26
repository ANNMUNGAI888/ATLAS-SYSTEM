import { useAuth } from "../../context/AuthContext";

function DepartmentDashboard() {
  const { logout } = useAuth();

  return (
    <div>
      <h1>ATLAS Dashboard</h1>

      <p>
        No tickets submitted yet.
      </p>

      <button onClick={logout}>
        Logout
      </button>
    </div>
  );
}

export default DepartmentDashboard;