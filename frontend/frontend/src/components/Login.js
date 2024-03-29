import React, { useState, useContext, useEffect } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import { reloadPage } from "../utils";
import "../styles/overallStyle.css";
import {
  BrowserRouter as Router,
  Routes,
  Navigate,
  Route,
  Link,
  useNavigate,
} from "react-router-dom";

import LoginForm from "./LoginForm";

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
      try {
        let response = await axios.post("http://localhost:8000/login", form);
        localStorage.setItem("userId", response.data.access_token);
        setCurrentUserID(response.data.access_token);
        Cookies.set("token", response.data.access_token);
        localStorage.setItem("isAuth", true);
        setAuth(true);
        return response;
      } catch (error) {
        setErrorMessage("Incorrect Username or password");
        setAuth(false);
      }
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
    <div className="text-center mt-5">
      {!auth ? <LoginForm setCurrentUserID={setCurrentUserID} /> : <></>}
    </div>
  );
};

export default Login;
