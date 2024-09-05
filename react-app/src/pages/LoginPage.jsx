// author: Jakub Rozkosz

import React, { useState } from "react";
import httpClient from "../httpClient";
import "./css_styles/AuthPage.css";

function LoginPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const logInUser = async () => {
        console.log(email, password);

        try {
            await httpClient.post("/login", {
                email,
                password,
            });

            window.location.href = "/";
        } catch (error) {
            if (error.response) {
                if (error.response.status === 401) {
                    alert("Invalid credentials");
                } else if (error.response.status === 403) {
                    alert(error.response.data.error);
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
            <h2>Log into your account</h2>
            <form className="auth-form">
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
                <button type="button" onClick={logInUser}>
                    Log in
                </button>
                <a href="/register" className="link-button">
                    Create a new account
                </a>
            </form>
        </div>
    );
}

export default LoginPage;
