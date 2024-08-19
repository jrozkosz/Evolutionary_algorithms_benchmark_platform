import React, { useState, useEffect } from "react";
// import { useParams } from "react-router-dom";
import httpClient from "../httpClient";


function AlgorithmRunningProgressPage() {
    // const { task_id } = useParams();
    const [user, setUser] = useState(null);
    const [progress, setProgress] = useState(null);

    useEffect(() => {
        (async () => {
            try {
            const resp = await httpClient.get("//localhost:5000/@me");
            setUser(resp.data);
            } catch (error) {
            console.log("Not authenticated");
            alert("You are not authenticated");
            window.location.href = "/";
            }
        })();
    }, []);

    useEffect(() => {
        const interval = setInterval(async () => {
            try {
                // console.log("before request")
                const response = await httpClient.get(`//localhost:5000/upload/progress`);
                // console.log("after request")
                const progress = response.data.progress;
                setProgress(progress);
                if (progress === 100) {
                    clearInterval(interval);
                }
            } catch (error) {
                if (error.response) {
                    alert(`${error.response.data.error}`);
                    window.location.href = "/";
                } else {
                    console.error("Error details:", error);
                    alert("An unexpected error occurred. Please try again later.");
                }
            }
        }, 5000);

        return () => clearInterval(interval);
    });

    return (
        <div>
            {progress !== null ? (
                <div>
                    <h2>Progress: {progress}%</h2>
                    {progress >= 100 && <p>Algorithm has completed successfully!</p>}
                    {/* tutaj dodać wyświetlanie wynikow przebiegu algorytmu */}
                    {/* wyslac zapytanie na nowo utworzony url w backendzie np. /alg_results ;albo w tym /upload/progress jakoś*/}
                </div>
            ) : (
                <p>Loading progress...</p>
            )}
        </div>
    );
};

export default AlgorithmRunningProgressPage;