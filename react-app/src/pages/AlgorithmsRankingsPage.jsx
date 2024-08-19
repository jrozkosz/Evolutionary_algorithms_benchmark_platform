import React, { useState, useEffect } from "react";
import httpClient from "../httpClient";
import Layout from "./Layout";
import { useOnMountUnsafe } from "../OnMountUnsafe";
import "./css_styles/AlgorithmsRankingsPage.css";


function AlgorithmsRankingsPage() {
    const [user, setUser] = useState(null);
    const [isAdmin, setIsAdmin] = useState(false);
    const [rankings, setRankings] = useState({
        cec_ranking: [],
        proposed_ranking: [],
        classic_ranking: [],
    });

    useOnMountUnsafe(() => {
        (async () => {
            try {
                const resp = await httpClient.get("//localhost:5000/@me");
                setUser(resp.data);
                setIsAdmin(resp.data.is_admin)
            } catch (error) {
                console.log("Not authenticated");
                alert("You are not authenticated");
                window.location.href = "/";
            }
        })();
    }, []);

    useEffect(() => {
        if(user != null) {
            (async () => {
                try {
                    const response = await httpClient.get("//localhost:5000/algorithms_rankings");
                    setRankings(response.data);
                } catch (error) {
                    if (error.response) {
                        alert(`An unexpected error occurred: ${error.response.status}`);
                    } else {
                        console.error("Error details:", error);
                        alert("An unexpected error occurred. Please try again later.");
                    }
                }
            })();
        }
    }, [user]);

    if(user == null) {
        return null;
    }

    return (
        <Layout is_admin={isAdmin}>
            <div className="page-container">
                <h2>CEC Ranking</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Username</th>
                            <th>Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rankings.cec_ranking.map((entry, index) => (
                            <tr key={index}>
                                <td>{entry.username}</td>
                                <td>{entry.score}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
    
                <h2>Proposed Ranking</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Username</th>
                            <th>Score</th>
                            <th>Optimum %</th>
                            <th>Thresholds %</th>
                            <th>Budget left %</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rankings.proposed_ranking.map((entry, index) => (
                            <tr key={index}>
                                <td>{entry.username}</td>
                                <td>{entry.score}</td>
                                <td>{entry.optimum}</td>
                                <td>{entry.threshold}</td>
                                <td>{entry.budget}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
    
                <h2>Classic Ranking</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Username</th>
                            <th>Average error</th>
                            <th>Median error</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rankings.classic_ranking.map((entry, index) => (
                            <tr key={index}>
                                <td>{entry.username}</td>
                                <td>{entry.average}</td>
                                <td>{entry.median}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Layout>
    );    
}

export default AlgorithmsRankingsPage;
