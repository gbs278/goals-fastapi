import React from "react";
import RegisterForm from "./RegisterForm";
import "../styles/overallStyle.css";
function Register() {
  return (
    <div className="text-center mt-5">
      <h1 className="header"> Registration</h1>
      <RegisterForm />
    </div>
  );
}

export default Register;
