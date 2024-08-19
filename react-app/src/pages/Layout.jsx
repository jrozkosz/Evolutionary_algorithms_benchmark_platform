import React from "react";
import Navbar from "./Navbar";

function Layout({ children, is_admin }) {
  return (
    <div>
      <Navbar is_admin={is_admin}/>
      <div>{children}</div>
    </div>
  );
}

export default Layout;
