import React, { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import axios from "axios";

function AddStepModal({ goalDescription, goalId }) {
  const [show, setShow] = useState(false);
  const [stepDescription, setStepDescription] = useState();
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  function handleChange(evt) {
    setStepDescription(evt.target.value);
  }
  function handleSubmit() {
    addStep();
    handleClose();
  }
  function refreshPage() {
    window.location.reload(false);
  }
  async function addStep() {
    // /api/create-step/{goal_id}"
    const data = {
      description: stepDescription,
      goal_id: goalId,
    };
    let res = await axios
      .post(`http://localhost:8000/api/create-step/${goalId}`, data, {
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
    refreshPage();
    return res;
  }

  return (
    <>
      <Button variant="primary" onClick={handleShow}>
        Add a step
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Add a step to {goalDescription}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form>
            <label>
              Step description
              <input type="text" name="description" onChange={handleChange} />
            </label>
          </form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSubmit}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
export default AddStepModal;
