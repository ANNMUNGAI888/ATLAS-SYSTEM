import AppRoutes from "./routes/AppRoutes";

function App() {
   console.log(import.meta.env.VITE_API_URL);
  
  return <AppRoutes />;
}

export default App;