// author: Jakub Rozkosz

import React, { useState, useEffect } from "react";
import httpClient from "../httpClient";
import Layout from "./Layout";
import { useOnMountUnsafe } from "../OnMountUnsafe";
import "./css_styles/SendingCodePage.css";

function SendingCodePage() {
	const [selectedFile, setSelectedFile] = useState(null);
	const [user, setUser] = useState(null);
	const [isAdmin, setIsAdmin] = useState(false);
	const [successMessage, setSuccessMessage] = useState("");
    const [information, setInformation] = useState("Loading uploaded algorithms...")
    const [uploadedAlgorithms, setAlgorithms] = useState({
        algorithms: []
    })

	useOnMountUnsafe(() => {
		(async () => {
			try {
				const resp = await httpClient.get("/auth/@me");
				setUser(resp.data);
				setIsAdmin(resp.data.is_admin);
			} catch (error) {
				console.log("Not authenticated");
				alert("You are not authenticated");
				window.location.href = "/";
			}
		})();
	}, []);

	useEffect(() => {
		if (user != null) {
			const interval = setInterval(async () => {
				try {
					const response = await httpClient.get("/algorithm/upload/progress");
					setAlgorithms(response.data);
                    if (uploadedAlgorithms.algorithms.length === 0) {
                        setInformation("No algorithms uploaded yet.");
                    }
					
					// if (progress >= 100) {
					// 	clearInterval(interval);
					// }
				} catch (error) {
                    if (error.response) {
                        if (error.response.status === 500) {
                            alert("We're sorry but we are having server issues. Please try again later.");
                        } else {
                            console.error("Error details:", error);
                            alert("An unexpected error occurred. Please try again later.");
                        }
                    }
                }
			}, 2000);

			return () => clearInterval(interval);
		}
	}, [user]);

    const handleDeletingAlgorithm = async (algorithm_id) => {
        try {
            await httpClient.post("/algorithm/delete_algorithm", {
                "algorithm_id": algorithm_id
            })

            const updatedAlgorithms = uploadedAlgorithms.algorithms.filter(algorithm => algorithm.id !== algorithm_id);
            setAlgorithms({ algorithms: updatedAlgorithms });

        } catch (error) {
            if(error.response) {
                if(error.response.status === 404) {
                    alert("Such algorithm does not exist.");
                }
            } else {
                alert("There was a problem with deleting an algorithm.")
            }
        }
    };

	const handleFileChange = (event) => {
		setSelectedFile(event.target.files[0]);
	};

	const handleFileUpload = async () => {
		if (!selectedFile) {
			alert("Please select a file to upload");
			return;
		}

		const formData = new FormData();
		formData.append("file", selectedFile);

		try {
			await httpClient.post("/algorithm/upload", formData);
			console.log("File uploaded successfully");

			setSuccessMessage("Sent successfully");

			setTimeout(() => {
				setSuccessMessage("");
			}, 5000);

		} catch (error) {
			console.log(error);
			if (error.response && error.response.status === 403) {
				alert("Algorithm already uploaded! You can submit only one implementation of an algorithm.");
			} else {
				alert("Failed to upload the file");
			}
		}
	};

	if (user == null) {
		return null;
	}

	return (
		<Layout is_admin={isAdmin}>
			<div className="upload-container">
				{user && (
					<>
						<input type="file" onChange={handleFileChange} />
						<button className="upload-button" onClick={handleFileUpload}>Send a file</button>
						{successMessage && <p className="upload-message">{successMessage}</p>}
					</>
				)}
                <h2>Uploaded algorithms:</h2>
				<div className="algorithms-container">
                    {uploadedAlgorithms.algorithms.length > 0 ? (
                        uploadedAlgorithms.algorithms.map((entry, index) => (
                            <div key={index} className="algorithm-entry">
                                <h3>{entry.name}</h3>
                                {entry.error ? (
                                    <p className="error-text">Error occurred. Please double check your algorithm interface and upload it again.</p>
                                ) : (
                                    <p className="progress-text">Running progress: {entry.progress}%</p>
                                )}
                                <button className="delete-button" onClick={() => handleDeletingAlgorithm(entry.id)}>Delete</button>
                            </div>
                        ))
                    ) : (
                        <p>{information}</p>
                    )}
                </div>
            </div>
        </Layout>
    );
}

export default SendingCodePage;
