import React, {useState, useEffect} from 'react'
import axios from 'axios'
function Register() {
    const [name, setName] = useState("");
    const [password, setPassword] = useState("");
    const [auth, setAuth] = useState()
    const handleSubmit = (evt) => {
      evt.preventDefault();
      const data = {
        name: name,
        password: password,
      };
      axios
        .post("http://localhost:8000/api/create-user", data)
        .then((response) => {
          alert("Sucessfully Registered");
        })
        .catch((error) => {
          alert("User Already Exists. Please Try Again");
        });
    };
    useEffect(() => {
      if(localStorage.getItem("isAuth")){
        setAuth(true)
      }
      else{
        setAuth(false)
      }
    }
    , [auth])
    return (
      <>
        {!auth ? 
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
          <div style={{ textAlign: "center" }}>Register Yourself</div>
          <br />
          <label>Username:</label>
          <input
            type="text"
            className="username"
            value={name}
            onChange={(e) => setName(e.target.value)}
          ></input>
          <br />
          <br />
          <label>Password: </label>
          <input
            type="password"
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
        : <></>}
      </>
    );
  } export default Register
  