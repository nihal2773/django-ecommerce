import { useState } from "react";
import API from "../api/axios";

function Login() {
  const [username, setUsername] = useState("admin001");
  const [password, setPassword] = useState("admin002");

  const handleLogin = () => {
    API.post("token/", {
      username: username,
      password: password,
    })
      .then((res) => {
        console.log(res.data);

        // store token
        localStorage.setItem("token", res.data.access);

        alert("Login successful");
      })
      .catch((err) => {
        console.log(err.response);
        alert("Login failed");
      });
  };

  return (
    <div>
      <h2>Login</h2>

      <input
        type="text"
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Login;