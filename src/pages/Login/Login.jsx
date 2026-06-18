import { useForm } from "react-hook-form";
import api from "../../api/axios";
function Login() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = async (data) => {
  try {
    const response = await api.post(
      "/auth/login",
      data
    );

    console.log(response.data);
  } catch (error) {
    console.error(error);
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

        <button type="submit">
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;