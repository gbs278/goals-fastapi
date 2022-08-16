import React , {useState, useEffect} from 'react';
import axios from 'axios'
function Goals({currentUserID, setCurrentUserID}){
    const [goals, setGoals] = useState()
    const [userId, setUserId] = useState("")

    // axios get to get goals
    const getGoals = async () => {
        const currentId = currentUserID || localStorage.getItem("userId")
        let res = await axios
            .get(`http://localhost:8000/api/get-goals/?id=${currentId}` , {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    mode: "no-cors"
                }
            } )
            .then((response) => {
                setGoals(response.data)
                return response;
            }
            )
            .catch((error) => {
                return error;
            }
            );
        return res;
    }

    useEffect(() => {
        if(localStorage.getItem("userId") && currentUserID.length === 0){ setCurrentUserID(localStorage.getItem("userId"))}
        setUserId(currentUserID)
        const currentGoals =  getGoals()
        

    }
    , [userId , localStorage.getItem("userId")])
    return (
        <div>
            <h1>Goals {currentUserID}</h1>
            {goals? 
                goals.map((goal, index) => {
                    return (
                        <div key={index}>
                            <h2>{goal.end_date}</h2>
                            <h3>{goal.description}</h3>
                        </div>
                    )
                }
                )
            : <h1>No goals</h1>}
        </div>
        

    )
} export default Goals;