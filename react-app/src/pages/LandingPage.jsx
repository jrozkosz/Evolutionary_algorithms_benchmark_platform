// author: Jakub Rozkosz

import React, { useState } from "react";
import httpClient from "../httpClient";
import Layout from "./Layout";
import { useOnMountUnsafe } from "../OnMountUnsafe";
import "./css_styles/LandingPage.css";

function LandingPage() {
    const [user, setUser] = useState(null);
    const [isAdmin, setIsAdmin] = useState(false);

    useOnMountUnsafe(() => {
        (async () => {
            try {
                const resp = await httpClient.get("/@me");
                setUser(resp.data);
                setIsAdmin(resp.data.is_admin);
                // window.location.href = "/upload";
            } catch (error) {
                console.log("Not authenticated");
            }
        })();
    }, []);

    // if (user !== null) {
    //     return (
    //         <Layout is_admin={isAdmin}>
    //             <div className="landing-page-wrapper">
    //                 <div className="landing-page">
    //                     <h1>Welcome to this Ranking Evolutionary Algorithms Application</h1>
    //                     <p>You are logged in</p>
    //                     <p><strong>ID: </strong>{user.id}</p>
    //                     <p><strong>Email: </strong>{user.email}</p>
    //                 </div>
    //             </div>
    //         </Layout>
    //     )
    // }

    return (
        <div className="landing-page-wrapper">
            <div className="landing-page">
                <h1>Welcome to this Ranking Evolutionary Algorithms Application</h1>
                <p>You are not logged in</p>
                <div>
                    <a href="/login">
                        <button className="landing-page-button">Login</button>
                    </a>
                    <a href="/register">
                        <button className="landing-page-button">Register</button>
                    </a>
                </div>
            </div>
        </div>
    );
    
}

export default LandingPage;
