// author: Jakub Rozkosz

import React, { useState } from "react";
import { useParams } from "react-router-dom";
import httpClient from "../httpClient";
import { useOnMountUnsafe } from "../OnMountUnsafe";

function ConfirmEmailPage() {
  const { token } = useParams();
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useOnMountUnsafe(() => {
    const confirmEmail = async () => {
      try {
        console.log("Request to Flask made...");
        const response = await httpClient.post(`/auth/confirm/${token}`);
        console.log(response.data)
        setMessage(response.data.info);
      } catch (error) {
        if (error.response.status === 500) {
          alert("We're sorry but we are having server issues. Please try again later.");
        } else {
        setError(error.response.data.error);
      }
    }
    };
    confirmEmail();
  });

  return (
    <div>
      {error && <h1>{error}</h1>}
      <h1>{message}</h1>
      {message && <p>You can now log into your account.</p>}
    </div>
  );
}

export default ConfirmEmailPage;