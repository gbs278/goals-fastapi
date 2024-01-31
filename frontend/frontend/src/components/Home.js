import React, { useState, useEffect } from "react";
import Cookies from "js-cookie";
import axios from "axios";
import "../styles/overallStyle.css";
import {
  BrowserRouter as Router,
  Routes,
  Navigate,
  Route,
  Link,
  useNavigate,
} from "react-router-dom";

function Home({ currentUserID, setCurrentUserID }) {
  const navigate = useNavigate();
  const [auth, setAuth] = useState();

  const handleOnClick = () => {
    localStorage.removeItem("isAuth");
    setAuth(false);
    Cookies.remove("token");
    navigate("/");
    window.location.reload();
  };

  useEffect(() => {
    if (localStorage.getItem("userId") && currentUserID.length === 0) {
      setCurrentUserID(localStorage.getItem("userId"));
    }
    if (!localStorage.getItem("isAuth")) {
      // Redirect to the login page if not authenticated
      navigate("/login");
    } else {
      setAuth(true);
    }
  }, [auth, currentUserID, navigate]);

  return (
    <>
      {!auth && <Navigate to="/login" />} {/* Redirect if not authenticated */}
      <div className="text-center mt-5">
        <h1 className="header">Home</h1>
        {auth ? <button onClick={handleOnClick}>Logout</button> : <></>}
      </div>
    </>
  );
}

export default Home;
