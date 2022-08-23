import React, { useState, useEffect } from "react";
import axios from "axios";
import Table from "react-bootstrap/Table";
import AddGoalModal from "./AddGoalModal";
function Goals({ currentUserID, setCurrentUserID }) {
  const [goals, setGoals] = useState();
  const [userId, setUserId] = useState("");

  // axios get to get goals
  const getGoals = async () => {
    const currentId = currentUserID || localStorage.getItem("userId");
    let res = await axios
      .get(`http://localhost:8000/api/get-goals/?id=${currentId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
          Accept: "application/json",
          mode: "no-cors",
        },
      })
      .then((response) => {
        setGoals(response.data);
        return response;
      })
      .catch((error) => {
        return error;
      });
    return res;
  };
  function handleRowClick(x, item) {
    console.log("clicked this row", item);
  }
  const headerTitleStyle = {
    textAlign: "center",
    alignSelf: "center",
  };
  useEffect(() => {
    if (localStorage.getItem("userId") && currentUserID.length === 0) {
      setCurrentUserID(localStorage.getItem("userId"));
    }
    setUserId(currentUserID);
    const currentGoals = getGoals();
  }, []);
  return (
    <div style={headerTitleStyle}>
      <h1>Goals</h1>
      <AddGoalModal />
      {goals && goals.length > 0 ? (
        <Table striped>
          <thead>
            <tr>
              <th>Description</th>
              <th>End Date</th>
            </tr>
          </thead>
          <tbody>
            {goals.map((item, i) => {
              return [
                <tr key={i} onClick={(x) => handleRowClick(x, item)}>
                  <td>{item.description}</td>
                  <td>{new Date(item.end_date).toDateString()}</td>
                </tr>,
              ];
            })}
            {/* goals.map((goal, index) => {
            return (
            <div key={index}>
              <h2>{goal.end_date}</h2>
              <h3>{goal.description}</h3>
            </div>
          );
        }) */}
          </tbody>
        </Table>
      ) : (
        <h1>No goals</h1>
      )}
    </div>
  );
}
export default Goals;
