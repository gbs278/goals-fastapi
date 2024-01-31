import React, { useState, useEffect } from "react";
import axios from "axios";
import ChangePasswordButton from "./ChangePasswordModal";
import "../styles/overallStyle.css";

function Profile({ currentUserID }) {
  const [userId, setUserId] = useState();
  const [username, setUsername] = useState();

  // method for axios get user profile
  const getUserProfile = async () => {
    const currentId = currentUserID || localStorage.getItem("userId");
    try {
      const response = await axios.get(
        `http://localhost:8000/api/get-user/${currentId}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
            Accept: "application/json",
            mode: "no-cors",
          },
        }
      );

      setUsername(response.data.name);
      return response;
    } catch (error) {
      return error;
    }
  };

  useEffect(() => {
    setUserId(currentUserID || localStorage.getItem("userId"));
    getUserProfile();
  }, [currentUserID, localStorage.getItem("userId")]);

  return (
    <div className="text-center mt-5">
      <div>
        <h1 className="header">Profile Name: {username}</h1>
        <ChangePasswordButton currentUserID={currentUserID} />
      </div>
    </div>
  );
}

export default Profile;
