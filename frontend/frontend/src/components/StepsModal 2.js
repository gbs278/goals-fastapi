import React, { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import axios from "axios";
import Table from "react-bootstrap/Table";
import AddStepModal from "./AddStepModal";
function StepsModal({ goalDescription, goalId, show, setShow }) {
  const [fullscreen, setFullscreen] = useState(true);
  const [steps, setSteps] = useState();

  async function getData() {
    console.log("in get data  ", goalId);
    let res = await axios
      .get(`http://localhost:8000/api/get-steps/{goal_id}?id=${goalId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
          Accept: "application/json",
          mode: "no-cors",
        },
      })
      .then((response) => {
        setSteps(response.data);
        return response;
      })
      .catch((error) => {
        return error;
      });
    return res;
  }
  useEffect(() => {
    if (show) {
      getData();
    }
  }, [show]);

  return (
    <>
      <Modal show={show} fullscreen={fullscreen} onHide={() => setShow(false)}>
        <Modal.Header closeButton>
          <Modal.Title>{goalDescription}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <AddStepModal goalDescription={goalDescription} goalId={goalId} />
          {steps && steps.length > 0 ? (
            <Table striped>
              <thead>
                <tr>
                  <th>Description</th>
                  <th>Done?</th>
                </tr>
              </thead>
              <tbody>
                {steps.map((item, i) => {
                  return [
                    <tr key={i}>
                      <td>{item.description}</td>
                      <td>{item.completed ? "Yes" : "No"}</td>
                    </tr>,
                  ];
                })}
              </tbody>
            </Table>
          ) : (
            <h1>No steps</h1>
          )}
        </Modal.Body>
      </Modal>
    </>
  );
}
export default StepsModal;
