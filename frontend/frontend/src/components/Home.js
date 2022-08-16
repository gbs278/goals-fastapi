import React  , {useState, useEffect} from 'react';
import Cookies from 'js-cookie'
import axios from 'axios'
import {
  BrowserRouter as Router,
  Routes,
  Navigate,
  Route,
  Link,
  useNavigate
} from "react-router-dom";
function Home({currentUserID, setCurrentUserID}){
  const navigate = useNavigate()
  const [auth, setAuth] = useState()
  const handleonclick = () => {
    localStorage.removeItem("isAuth")
    setAuth(false)
    Cookies.remove("token");
    navigate("/")
    window.location.reload()

  };
  useEffect(() => {
    if(localStorage.getItem("userId") && currentUserID.length === 0){ setCurrentUserID(localStorage.getItem("userId"))}
    if(localStorage.getItem("isAuth")){
      setAuth(true)
    }
    else{
      setAuth(false)
    }
    navigate("/")
  }

  , [auth, currentUserID])
  return (
    <>
  <h1>Home
  </h1>
  {auth ? <button onClick={handleonclick}>Logout</button> : <></>}
  </>
  )
} export default Home
