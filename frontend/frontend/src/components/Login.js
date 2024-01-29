import React, { useState, useContext, useEffect } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import { reloadPage } from "../utils";
import {
  BrowserRouter as Router,
  Routes,
  Navigate,
  Route,
  Link,
  useNavigate,
} from "react-router-dom";
const Login = ({ setCurrentUserID }) => {
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [auth, setAuth] = useState();
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState(null);
  const handleSubmit = async (evt) => {
    if (evt) {
      evt.preventDefault();
    }
    const data = {
      username: name,
      password: password,
    };
    const form = new FormData();
    form.append("username", name);
    form.append("password", password);
    const news = async () => {
      let res = await axios
        .post("http://localhost:8000/login", form)
        .then((response) => {
          localStorage.setItem("userId", response.data.access_token);
          setCurrentUserID(response.data.access_token);
          Cookies.set("token", response.data.access_token);
          localStorage.setItem("isAuth", true);
          setAuth(true);
          return response;
        })
        .catch((error) => {
          // alert("Incorrect Username or password", error);
          setErrorMessage("Incorrect Username or password");
          setAuth(false);
        });
      return res;
    };
    let x = await news();
    if (x) {
      navigate("/");
      reloadPage();
      localStorage.setItem("isAuth", false);
      setErrorMessage(null);
      setAuth(false);
    }
  };
  useEffect(() => {
    if (localStorage.getItem("isAuth")) {
      setAuth(true);
    } else {
      setAuth(false);
    }
  }, [auth]);
  return (
    <>
      {!auth ? (
        <form
          style={{
            marginTop: "100px",
            marginLeft: "50px",
            border: "solid 1px",
            width: "max-content",
            borderColor: "green",
          }}
          onSubmit={handleSubmit}
        >
          {errorMessage && <div>{errorMessage}</div>}
          <div style={{ textAlign: "center" }}>Login</div>
          <br />
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            className="username"
            value={name}
            onChange={(e) => setName(e.target.value)}
          ></input>

          <br />
          <br />
          <label htmlFor="password">Password: </label>
          <input
            type="password"
            id="password"
            className="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          ></input>
          <br />
          <br />
          <div style={{ textAlign: "center" }}>
            <input type="submit" value="Submit" />
          </div>
        </form>
      ) : (
        <></>
      )}
    </>
  );
};
export default Login;
