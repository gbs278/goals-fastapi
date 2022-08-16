import {
  BrowserRouter as Router,
  Routes,
  Navigate,
  Route,
  Link,
} from "react-router-dom";
import React, { useState, Fragment } from "react";
import Register from './components/Register'
import Login from './components/Login'
import axios from "axios";
import Home from './components/Home'
import Cookies from 'js-cookie'
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';
import Profile from './components/Profile'
import Goals from './components/Goals'
import NavDropdown from 'react-bootstrap/NavDropdown';

function App() {
  const [auth, setAuth] = useState(false);
  const [token, setToken] = useState("");
  const [currentUserID, setCurrentUserID] = useState("");
  
  React.useEffect(() => {
    
    Cookies.set(false)
    if(localStorage.getItem("isAuth")){
      setAuth(true)
    }
    else{
      setAuth(false)
    }
    
  }, [ localStorage.getItem("isAuth"), auth, currentUserID]);
return (
    <>
        {!auth? <AllLinks /> : <OnlyHome/>}
       
        <AppRoutes auth={auth} setCurrentUserID={setCurrentUserID} currentUserID={currentUserID} />
       
       
    
       
    </>
  );
} export default App;


function AllLinks(){
  return(
    <>
  <Navbar bg="primary" variant="dark">
    <Container>
      <Navbar.Brand href="/">Home</Navbar.Brand>
      <Nav className="me-auto">
        
        <Nav.Link href="/register">Register</Nav.Link>
        <Nav.Link href="/login">Login</Nav.Link>
      </Nav>
    </Container>
  </Navbar>

  
</>
  )
}

function OnlyHome(){
 return(
  <>
  <Navbar bg="primary" variant="dark" >
    <Container>
      <Navbar.Brand href="/">Home</Navbar.Brand>
      <Nav.Link href="/goals">Goals</Nav.Link>
      <Nav.Link href="/profile">Profile</Nav.Link>
    </Container>
  </Navbar>

  
</>
 )
}



const AppRoutes = ({auth, currentUserID, setCurrentUserID}) => {
  
  return (
    <Router>
    <Routes>
      {!auth ? 
      <>
      <Route  path="/register" element={<Register />} />
      <Route  path="/login" element={<Login setCurrentUserID={setCurrentUserID}/>} />
      </>
       : 
       <>
       <Route exact path ="/goals" element={<Goals currentUserID={currentUserID} setCurrentUserID={setCurrentUserID}/>} />
       <Route exact path ="/profile" element={<Profile currentUserID={currentUserID}/>} />
       </>
       }
      <Route path = "/" element ={<Home currentUserID={currentUserID} setCurrentUserID={setCurrentUserID} />} />
      {/* <Route path="*" element={ <Navigate to="/" />}/> */}
         
    </Routes>
    </Router>
  );
};

