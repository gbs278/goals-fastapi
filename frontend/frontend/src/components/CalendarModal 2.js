import React, { useState } from "react";
import Calendar from "react-calendar";
import Modal from "react-bootstrap/Modal";
function CalendarModal({ showCalendar, setShowCalendar, date, setDate }) {
  const handleClose = () => setShowCalendar(false);
  const handleShow = () => setShowCalendar(true);

  function gal(evt) {
    setDate(evt);
    console.log(date);
    handleClose();
  }

  return (
    <Modal show={showCalendar} onHide={handleClose}>
      <Modal.Header closeButton title="Calendar">
        <Modal.Title>Pick an end Date</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div>
          <Calendar onChange={gal} value={date} />
        </div>
      </Modal.Body>
    </Modal>
  );
}
export default CalendarModal;

{
  /* <Modal show={show} onHide={handleClose}>
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
    <Button onClick={openCalendar}>Set End Date</Button>
  </Modal.Body>
  <Modal.Footer>
    <Button variant="secondary" onClick={handleClose}>
      Close
    </Button>
    <Button variant="primary" onClick={handleSubmit}>
      Save Changes
    </Button>
  </Modal.Footer>
</Modal>; */
}
