import React, { useState } from "react";
import Login from "./Login";
import SignUp from "./SignUp";

import "./Modale.css";
const Modale = (props) => {
  const [showLogin, setShowLogin] = useState(true);
  const [showSignUp, setShowSignUp] = useState(false);

  if (!props.show) {
    return null;
  } else {
    if (showLogin === true && showSignUp === false) {
      return (
        <Login
          show={props.show}
          onClose={props.onClose}
          setShowLogin={setShowLogin}
          setShowSignUp={setShowSignUp}
        />
      );
    } else {
      return (
        <SignUp
          show={props.show}
          onClose={props.onClose}
          setShowLogin={setShowLogin}
          setShowSignUp={setShowSignUp}
        />
      );
    }
  }
};

export default Modale;
