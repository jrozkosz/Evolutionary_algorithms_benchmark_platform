// author: Jakub Rozkosz

import React, { useState, useEffect } from "react";
import httpClient from "../httpClient";
import Layout from "./Layout";
import { useOnMountUnsafe } from "../OnMountUnsafe";
import "./css_styles/AdminPanelPage.css";


function AdminPanelPage() {
    const [admin, setAdmin] = useState(null);
    const [isAdmin, setIsAdmin] = useState(false);
    const [infoText, setInfoText] = useState("");
    const [isCrucial, setIsCrucial] = useState(false);
    const [users, setUsers] = useState([]);

    useOnMountUnsafe(() => {
        (async () => {
            try {
                const resp = await httpClient.get("/@me");
                setAdmin(resp.data);
                setIsAdmin(resp.data.is_admin);
                console.log(isAdmin);
            } catch (error) {
                console.log("Not authenticated");
                alert("You are not authenticated");
                window.location.href = "/";
            }
        })();
    }, []);

    useEffect(() => {
        if(isAdmin) {
            (async () => {
                try {
                    const resp = await httpClient.get("/display_users");
                    setUsers(resp.data.users);
                } catch (error) {
                    console.log("Error fetching users", error);
                    alert("There was a problem with fetching users.");
                }
            })();
    }
    }, [isAdmin]);

    const addInfoText = async () => {
        try {
            await httpClient.post("/add_info", {
                infoText,
                isCrucial
            });
            console.log("Information added successfully");
            window.location.href = "/information";
        } catch (error) {
            if (error.response.status === 400) {
                alert("Text cannot be empty!");
            } else {
                alert("There was a problem with adding an info.");
            }
        }
    };

    const deleteUser = async (user_id) => {
        try {
            await httpClient.post("/delete_user", {
                "user_id": user_id
            });
            setUsers(users.filter(user => user.id !== user_id));
        } catch (error) {
            if(error.response) {
                if(error.response.status === 404) {
                    alert("Such user does not exist.");
                }
            } else {
                alert("There was a problem with deleting a user.")
            }
        }
    };

    if(!isAdmin) {
        return null;
    }

    return (
        <Layout is_admin={isAdmin}>
            <div className="admin-panel-container">
                <div className="user-list">
                    <h2>Users List</h2>
                    <div className="user-list-content">
                        {users.map((user, index) => (
                            <div key={index} className="user-item">
                                <button className="user-item-button" onClick={() => deleteUser(user.id)}>Delete</button>
                                <p><strong>Username:</strong> {user.username}</p>
                                <p><strong>Email:</strong> {user.email}</p>
                                <p><strong>Algorithms Sent:</strong> {user.algorithms_sent}</p>
                                <p><strong>Running Progress:</strong> {user.running_progress}%</p>
                            </div>
                        ))}
                    </div>
                </div>
                <div className="info-form">
                    <div>
                        <label htmlFor="infoText">Information Text:</label>
                        <textarea
                            id="infoText"
                            value={infoText}
                            onChange={(e) => setInfoText(e.target.value)}
                            placeholder="Enter information text..."
                        ></textarea>
                    </div>
                    <div>
                        <label htmlFor="isCrucial">Is Crucial:</label>
                        <input
                            type="checkbox"
                            id="isCrucial"
                            checked={isCrucial}
                            onChange={(e) => setIsCrucial(e.target.checked)}
                        />
                    </div>
                    <button onClick={addInfoText}>Add info text to Information</button>
                </div>
            </div>
        </Layout>
    );
}

export default AdminPanelPage;
