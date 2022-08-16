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
    console.log("clicked")
    localStorage.removeItem("isAuth")
    setAuth(false)
    console.log("removed" , localStorage.getItem("isAuth"))
    Cookies.remove("token");
    navigate("/")
    window.location.reload()

  };
  useEffect(() => {
    if(localStorage.getItem("userId") && currentUserID.length === 0){ setCurrentUserID(localStorage.getItem("userId"))}
    console.log("in home user id" , currentUserID)
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
// function Home(){
//     const [data, setData] = useState("");
//     console.log("penis token api" , {TokenApi})
//     const handleonclick = () => {
//       Auth.setAuth(false);
//       Cookies.remove("token");
//     };
//    // httpslet toke = Token.token;
//     const headers = {
//       Authorization: `Bearer `, // include toke
//     };
//     const getdata = async () => {
//       let res = await axios
//         .get("http://127.0.0.1:8000/", { headers })
//         .then((response) => {
//           return response.data.data;
//         });
//       return res;
//     };
//     // const readCookie = () => {
//     //   let token = Cookies.get("token");
//     //   if (token) {
//     //     setAuth(true);
//     //     setToken(token);
//     //   }
//     // };
//     useEffect(async () => {
//       let x = await getdata();
//       setData(x);
//       // readCookie()
//       console.log(x);
//     }, []);
//     return (
//       <>
//         <h2>Home</h2>
//         <button onClick={handleonclick}>Logout</button>
//         <h1>{data}</h1>
//       </>
//     );
// } export default Home;