import React, { useState, useEffect } from "react";
import axios from "axios";
import Table from "react-bootstrap/Table";
import AddGoalModal from "./AddGoalModal";
import StepsModal from "./StepsModal";
import GoalProgressBar from "./GoalProgressBar";
import Button from "react-bootstrap/Button";
function Goals({ currentUserID, setCurrentUserID }) {
  const [goals, setGoals] = useState();
  const [userId, setUserId] = useState("");
  const [showSteps, setShowSteps] = useState(false);
  const [goalId, setGoalId] = useState();
  const [goalDescription, setGoalDescription] = useState();

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

  function refreshPage() {
    window.location.reload(false);
  }

  async function deleteGoal(goal) {
    let res = axios
      .delete(`http://localhost:8000/api/delete-goal/{goal_id}?id=${goal._id}`)
      .then((response) => {
        return response;
      })
      .catch((error) => {
        return error;
      });
    return res;
  }

  function deleteAndRefresh(goal) {
    deleteGoal(goal);
    refreshPage();
  }

  function handleRowClick(x, item) {
    console.log("clicked ", item.description);
    setGoalDescription(item.description);
    setShowSteps(true);
    setGoalId(item._id);
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
              <th>Progress</th>
              <th>Delete goal?</th>
            </tr>
          </thead>
          <tbody>
            {goals.map((item, i) => {
              return [
                <tr key={i} onClick={(x) => handleRowClick(x, item)}>
                  <td>{item.description}</td>
                  <td>{new Date(item.end_date).toDateString()}</td>
                  <td>
                    <GoalProgressBar goal={item} />
                  </td>
                  <td>
                    <button onClick={(e) => deleteAndRefresh(item)}>
                      Delete
                    </button>
                  </td>
                </tr>,
              ];
            })}
          </tbody>
        </Table>
      ) : (
        <h1>No goals</h1>
      )}
      <StepsModal
        goalDescription={goalDescription}
        goalId={goalId}
        show={showSteps}
        setShow={setShowSteps}
      />
    </div>
  );
}
export default Goals;
