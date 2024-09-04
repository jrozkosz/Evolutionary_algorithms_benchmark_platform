// author: Jakub Rozkosz

import React from "react";
import { Link } from "react-router-dom";
import httpClient from "../httpClient";
import "./css_styles/Navbar.css";

function Navbar({ is_admin }) {

  const logoutUser = async () => {
    await httpClient.post("//localhost:5000/logout");
    window.location.href = "/";
  };

  return (
    <div className="navbar-container">
      <nav className="navbar">
        <ul className="navbar-list">
          <li className="navbar-item"><Link to="/">Home</Link></li>
          <li className="navbar-item"><Link to="/information">Information</Link></li>
          <li className="navbar-item"><Link to="/upload">Upload</Link></li>
          <li className="navbar-item"><Link to="/algorithms_rankings">Rankings</Link></li>
          {is_admin && (
            <li className="navbar-item"><Link to="/admin_panel">Admin Panel</Link></li>
          )}
        </ul>
      </nav>
      <div className="navbar-logout-button">
        <button onClick={logoutUser}>Log out</button>
      </div>
    </div>
  );
}

export default Navbar;
