// author: Jakub Rozkosz

import React, { useState } from "react";
import httpClient from "../httpClient";
import "./css_styles/AuthPage.css";

function RegisterPage() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    const registerUser = async () => {
        try {
            await httpClient.post("/auth/register", {
                username,
                email,
                password,
            });
            setMessage("If the submitted email is valid, a confirmation mail should be sent. Please go to your mailbox and confirm.");
        } catch (error) {
            if (error.response) {
                if (error.response.status === 401) {
                alert("None of the values can be empty")
                } else if (error.response.status === 409) {
                    alert("Such user already exists");
                } else if (error.response.status === 500) {
                    alert("We're sorry but we are having server issues. Please try again later.");
                }
            } else {
                console.error("Error details:", error);
                alert("An unexpected error occurred. Please try again later.");
            }
        }
    };

    return (
        <div className="auth-page">
            <h1>Welcome to the Evolutionary Algorithms Ranking App</h1>
            <h2>Create an account</h2>
            {message && <p className="message">{message}</p>}
            <form className="auth-form">
                <div>
                    <label>Username: </label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div>
                    <label>Email: </label>
                    <input
                        type="text"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div>
                    <label>Password: </label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="button" onClick={registerUser}>
                    Register
                </button>
                <a href="/login" className="link-button">
                    Log into your account
                </a>
            </form>
        </div>
    );
}

export default RegisterPage;
