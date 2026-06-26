import { useState } from "react";
import { useForm } from "react-hook-form";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

const DEMO_USER = {
  deptCode: "FIN",
  password: "123456",
};

function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [loginError, setLoginError] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => {
    if (
      data.deptCode === DEMO_USER.deptCode &&
      data.password === DEMO_USER.password
    ) {
      // Clear any previous error
      setLoginError("");

      // Store fake JWT
      login("fake-jwt-token");

      // Redirect to dashboard
      navigate("/dashboard");
    } else {
      setLoginError(
        "Department code or password is incorrect"
      );
    }
  };

  return (
    <div className="login-container">
      <h2>ATLAS Login</h2>

      <form onSubmit={handleSubmit(onSubmit)}>
        <div>
          <label>Department Code</label>

          <input
            type="text"
            {...register("deptCode", {
              required: "Department code is required",
            })}
          />

          {errors.deptCode && (
            <p>{errors.deptCode.message}</p>
          )}
        </div>

        <div>
          <label>Password</label>

          <input
            type="password"
            {...register("password", {
              required: "Password is required",
            })}
          />

          {errors.password && (
            <p>{errors.password.message}</p>
          )}
        </div>

        {/* Login Error Message */}
        {loginError && (
          <p
            style={{
              color: "red",
              marginTop: "10px",
            }}
          >
            {loginError}
          </p>
        )}

        <button type="submit">
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;