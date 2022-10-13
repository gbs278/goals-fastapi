import React, { useState, useEffect } from "react";
import axios from "axios";
function CompleteStep({ step }) {
  function refreshPage() {
    window.location.reload(false);
  }
  async function updateGoal() {
    let res = await axios
      .put(
        `http://localhost:8000/api/increment-completed-steps/${step.goal_id}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
            Accept: "application/json",
            mode: "no-cors",
          },
        }
      )
      .then((response) => {
        return response;
      })
      .catch((error) => {
        return error;
      });
    console.log("gal got res", res.data);
    return res;
  }

  async function updateStep() {
    const data = {
      completed: true,
    };
    let res = await axios
      .put(`http://localhost:8000/api/update-step/${step._id}`, data, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
          Accept: "application/json",
          mode: "no-cors",
        },
      })
      .then((response) => {
        return response;
      })
      .catch((error) => {
        return error;
      });
    console.log("gal got res", res.data);
    return res;
  }

  function handleClick() {
    updateStep();
    updateGoal();
  }

  useEffect(() => {}, []);

  return <button onClick={(e) => handleClick()}> Complete Step</button>;
}
export default CompleteStep;
