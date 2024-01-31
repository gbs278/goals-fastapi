import React, { useState, useContext, useEffect } from "react";
import {
  MDBContainer,
  MDBInput,
  MDBCheckbox,
  MDBBtn,
  MDBIcon,
} from "mdb-react-ui-kit";

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

function LoginForm({ setCurrentUserID }) {
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [auth, setAuth] = useState();
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState(null);
  const handleSubmit = async (evt) => {
    // console.log("done, name ", name, " password ", password);
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

    // Remove the setErrorMessage("Incorrect Username or password"); line

    const news = async () => {
      try {
        let response = await axios.post("http://localhost:8000/login", form);
        localStorage.setItem("userId", response.data.access_token);
        setCurrentUserID(response.data.access_token);
        Cookies.set("token", response.data.access_token);
        localStorage.setItem("isAuth", true);
        setAuth(true);
        // Remove the setErrorMessage(null); line
        return response;
      } catch (error) {
        // Remove the setErrorMessage("Incorrect Username or password"); line
        setErrorMessage("Wrong Password or Username");
        setAuth(false);
      }
    };

    // Add a condition to show the "Wrong Password" message
    <div className="text-danger">{!auth && "Wrong Password"}</div>;

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
    <div>
      <div className="text-danger">{errorMessage && errorMessage}</div>
      <MDBContainer className="p-3 my-5 d-flex flex-column w-50">
        <MDBInput
          wrapperClass="mb-4"
          label="Username"
          id="form1"
          type="email"
          onChange={(e) => setName(e.target.value)}
          labelClass="text-light"
        />

        <MDBInput
          wrapperClass="mb-4"
          label="Password"
          id="form2"
          type="password"
          onChange={(e) => setPassword(e.target.value)}
          labelClass="text-light"
        />

        <MDBBtn type="submit" onClick={handleSubmit} className="mb-4">
          Sign in
        </MDBBtn>

        <div className="text-center">
          <p>
            Not a member? <a href="/register">Register</a>
          </p>
        </div>
      </MDBContainer>
    </div>
  );
}

export default LoginForm;
