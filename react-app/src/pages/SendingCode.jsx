import React, { useState, useEffect } from "react";
import httpClient from "../httpClient";

function SendCode() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [user, setUser] = useState(null);

    useEffect(() => {
        (async () => {
            try {
            const resp = await httpClient.get("//localhost:5000/@me");
            setUser(resp.data);
            } catch (error) {
            console.log("Not authenticated");
            alert("You are not authenticated");
            }
        })();
    }, []);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    if (!selectedFile) {
      alert("Wybierz plik do przesłania");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      httpClient.post("//localhost:5000/upload", formData);
      console.log("Plik został przesłany pomyślnie");
    } catch (error) {
    //   if (error.response.status === 401) {
    //     alert("Invalid credentials");
    // }
      console.log("Failed to upload a file");
    }
    // httpClient.post("//localhost:5000/upload", formData)
    //   .then((response) => {
    //     // Obsługa odpowiedzi z backendu po przesłaniu pliku
    //     console.log("Plik został przesłany pomyślnie");
    //   })
    //   .catch((error) => {
    //     // Obsługa błędów
    //     console.error("Wystąpił błąd podczas przesyłania pliku", error);
    //   });
  };

    // const handleNotAuthenticated = () => {
    //     alert("You are not authenticated");
    // }

  return (
    <div>
        {user != null ? (
            <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleFileUpload}>Send a file</button>
            </div>
        ) : null}
        {/* // ) : (
        //     <div>
        //     {/* <p>You are not logged in</p> */}
    </div>
    // )} */}
  );
}

export default SendCode;
