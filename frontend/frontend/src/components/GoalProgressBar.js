import ProgressBar from "react-bootstrap/ProgressBar";
import React, { useState, useEffect } from "react";
function GoalProgressBar({ goal }) {
  const [now, setNow] = useState(0);

  function getNow() {
    if (goal.completed_steps <= 0) {
      setNow(0);
    }
    if (goal.steps.length === 0) {
      setNow(0);
    } else {
      setNow(Math.floor((goal.completed_steps / goal.steps.length) * 100));
    }
    console.log("gal in getNow ", goal);
  }
  useEffect(() => {
    getNow();
  }, []);
  return <ProgressBar now={now} label={`${now}%`} />;
}

export default GoalProgressBar;
