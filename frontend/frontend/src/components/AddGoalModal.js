import React, { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import axios from "axios";
import CalendarModal from "./CalendarModal";
function AddGoalModal({ currentUserID }) {
  const [show, setShow] = useState(false);
  const [userId, setUserId] = useState();
  const [showCalendar, setShowCalendar] = useState(false);
  const [date, setDate] = useState(new Date());
  const [description, setDescription] = useState("");
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  function handleChange(event) {
    event.preventDefault();
    setDescription(event.target.value);
  }
  async function handleSubmit(event) {
    event.preventDefault();
    // call axios to update password for username
    let newDate = date.toLocaleDateString();
    console.log("before parse", newDate);
    newDate = newDate.split("/");
    if (newDate.length < 3) {
      alert("Please enter a valid date");
      return newDate;
    }
    newDate = newDate[2] + "-" + newDate[0] + "-" + newDate[1];
    console.log("submitted", { date });
    const data = {
      description: description,
      user_id: userId,
      end_date: newDate,
    };
    console.log(data);
    let res = await axios

      .post(
        `http://localhost:8000/api/create-goal/{id}?user_id=${userId}`,
        data,
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
    handleClose();
    return res;
  }
  function openCalendar() {
    setShowCalendar(true);
  }
  // make useeffect
  useEffect(() => {
    setUserId(currentUserID || localStorage.getItem("userId"));
  }, [currentUserID, show]);
  return (
    <>
      <Button variant="primary" onClick={handleShow}>
        Add Goal
      </Button>
      <CalendarModal
        showCalendar={showCalendar}
        setShowCalendar={setShowCalendar}
        date={date}
        setDate={setDate}
      />
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Add Goal</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form>
            <label>
              Description
              <input type="text" name="description" onChange={handleChange} />
            </label>
          </form>
          Complete By:{" "}
          <Button onClick={openCalendar}>{date.toDateString()}</Button>
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

export default AddGoalModal;
