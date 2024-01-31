// RegisterForm.jsx
import React, { useState, useEffect } from "react";
import axios from "axios";
import { MDBContainer, MDBInput, MDBBtn } from "mdb-react-ui-kit";
import { reloadPage } from "../utils";

function RegisterForm() {
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [successMessage, setSuccessMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  const handleSubmit = async (evt) => {
    evt.preventDefault();
    const data = {
      name: name,
      password: password,
    };

    try {
      let response = await axios.post(
        "http://localhost:8000/api/create-user",
        data
      );
      setErrorMessage(null);
      setSuccessMessage("Successfully Registered");
    } catch (error) {
      setSuccessMessage(null);
      setErrorMessage("User Already Exists. Please Try Again");
    }
  };

  return (
    <MDBContainer className="p-3 my-5 d-flex flex-column w-50">
      {successMessage && <div>{successMessage}</div>}
      {errorMessage && <div>{errorMessage}</div>}
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
        Register
      </MDBBtn>
    </MDBContainer>
  );
}

export default RegisterForm;
