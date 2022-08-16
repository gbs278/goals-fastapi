import React, { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import axios from "axios";
function Example({ currentUserID }) {
  const [show, setShow] = useState(false);
  const [newPassword, setNewPassword] = useState();
  const [userId, setUserId] = useState();
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  function handleChange(event) {
    event.preventDefault();
    setNewPassword(event.target.value);
  }
  async function handleSubmit(event) {
    event.preventDefault();
    // call axios to update password for username
    const data = {
      password: newPassword,
    };
    let res = await axios
      .put(`http://localhost:8000/api/update-user/${userId}`, data, {
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
    handleClose();
    return res;
  }
  // make useeffect
  useEffect(() => {
    setUserId(currentUserID || localStorage.getItem("userId"));
  }, [currentUserID, show]);
  return (
    <>
      <Button variant="primary" onClick={handleShow}>
        Change Password
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Change Password</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form>
            <label>
              Password:
              <input type="password" name="name" onChange={handleChange} />
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

export default Example;
