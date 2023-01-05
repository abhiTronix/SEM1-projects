import React, { useState } from "react";
import AdminLogin from "./AdminLogin";
import AdminSignUp from "./AdminSignUp";

import "./Modale.css";
const AdminModale = (props) => {
  const [showLogin, setShowLogin] = useState(true);
  const [showSignUp, setShowSignUp] = useState(false);

  if (!props.show) {
    return null;
  } else {
    if (showLogin === true && showSignUp === false) {
      return (
        <AdminLogin
          show={props.show}
          onClose={props.onClose}
          setShowLogin={setShowLogin}
          setShowSignUp={setShowSignUp}
        />
      );
    } else {
      return (
        <AdminSignUp
          show={props.show}
          onClose={props.onClose}
          setShowLogin={setShowLogin}
          setShowSignUp={setShowSignUp}
        />
      );
    }
  }
};

export default AdminModale;
