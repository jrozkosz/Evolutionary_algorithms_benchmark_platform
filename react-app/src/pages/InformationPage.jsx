// author: Jakub Rozkosz

import React, { useEffect, useState } from "react";
import httpClient from "../httpClient";
import Layout from "./Layout";
import { useOnMountUnsafe } from "../OnMountUnsafe";
import "./css_styles/InformationPage.css";

function InformationPage() {
    const [user, setUser] = useState(null);
    const [isAdmin, setIsAdmin] = useState(false);
    const [texts, setTexts] = useState([]);

    useOnMountUnsafe(() => {
        (async () => {
            try {
                const resp = await httpClient.get("/@me");
                setUser(resp.data);
                setIsAdmin(resp.data.is_admin);
            } catch (error) {
                console.log("Not authenticated");
                alert("You are not authenticated");
                window.location.href = "/";
            }
        })();
    }, [])

    useEffect(() => {
        if(user != null) {
            (async () => {
                try {
                    const resp = await httpClient.get("/information");
                    setTexts(resp.data.texts);
                    console.log(resp.data.texts);
                } catch (error) {
                    console.error("Error fetching information", error);
                }
            })();
        }
    }, [user])

    if (user == null) {
        return null;
    }

    const deleteInformation = async (info_id) => {
        try {
            await httpClient.post("/delete_info", {
                info_id
            });
            setTexts(texts.filter(text => text.id !== info_id));
        } catch (error) {
            if(error.response.data.error === "User not found") {
                alert("Such information does not exist.");
            } else {
                alert("There was a problem with deleting an information.")
            }
        }
    };

    return (
        <Layout is_admin={isAdmin}>
            <div className="information-page">
                <h1>Information</h1>
                <div className="information-cards">
                    {texts.map((info, index) => (
                        <div className={`information-card ${info.is_crucial ? 'crucial' : ''}`} key={index}>
                            {isAdmin && <button className="information-button" onClick={() => deleteInformation(info.id)}>Delete</button>}
                            <p className="information-text">{info.text}</p>
                            <p className="information-date"><em>Added on: {new Date(info.added_date).toLocaleString()}</em></p>
                        </div>
                    ))}
                </div>
            </div>
        </Layout>
    )
}

export default InformationPage;
