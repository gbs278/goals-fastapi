import React, { useState, useEffect } from "react";
import axios from "axios";
import Example from "./ChangePasswordModal";
function Profile({ currentUserID }) {
  const [userId, setUserId] = useState();
  const [username, setUsername] = useState();
  // method for axios get user profile
  const getUserProfile = async () => {
    const currentId = currentUserID || localStorage.getItem("userId");
    let res = await axios
      .get(`http://localhost:8000/api/get-user/${currentId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
          Accept: "application/json",
          mode: "no-cors",
        },
      })
      .then((response) => {
        setUsername(response.data.name);
        return response;
      })
      .catch((error) => {
        return error;
      });
    return res;
  };
  useEffect(() => {
    setUserId(currentUserID || localStorage.getItem("userId"));
    const gal = getUserProfile();
  }, [userId, localStorage.getItem("userId")]);
  return (
    <>
      <h1>Profile Name: {username}</h1>
      <Example currentUserID={currentUserID} />
    </>
  );
}
export default Profile;
