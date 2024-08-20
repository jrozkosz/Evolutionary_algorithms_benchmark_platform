import React, { useState, useEffect } from "react";
import httpClient from "../httpClient";
import Layout from "./Layout";
import { useOnMountUnsafe } from "../OnMountUnsafe";
import "./css_styles/SendingCodePage.css";

function SendingCodePage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [user, setUser] = useState(null);
  const [progress, setProgress] = useState(null);
  const [notUploaded, setNotUploaded] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [information, setInformation] = useState("A file has not been uploaded yet.")

  useOnMountUnsafe(() => {
    (async () => {
      try {
        const resp = await httpClient.get("//localhost:5000/@me");
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
          const response = await httpClient.get("//localhost:5000/upload/progress");
          const progress = response.data.progress;
          setNotUploaded(false);
          setProgress(progress);
          if (progress >= 100) {
            clearInterval(interval);
          }
        } catch (error) {
          if (error.response.data.error === "Algorithm has not yet been uploaded") {
            setNotUploaded(true);
            clearInterval(interval);
          } else if (error.response.data.error ===  "An error occurred when processing the algorithm") {
            setNotUploaded(true);
            setInformation("An error occurred when processing the algorithm. Please double check whether your \
              algorithm interface is correct and send your code again.");
            clearInterval(interval);
          }
          else {
            console.error("Error details:", error);
            alert("An unexpected error occurred. Please try again later.");
          }
        }
      }, 1000);

      return () => clearInterval(interval);
    }
  }, [user]);

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
      await httpClient.post("//localhost:5000/upload", formData);
      console.log("File uploaded successfully");

      setSuccessMessage("Sent successfully");
      setNotUploaded(false);

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
        <div>
          {notUploaded ? (
            <p>{information}</p>
          ) : progress !== null ? (
            <div>
              <h2>Progress: {progress}%</h2>
              {progress >= 100 && <p>Algorithm has completed successfully!</p>}
            </div>
          ) : (
            <p>Loading progress...</p>
          )}
        </div>
      </div>
    </Layout>
  );
}

export default SendingCodePage;
