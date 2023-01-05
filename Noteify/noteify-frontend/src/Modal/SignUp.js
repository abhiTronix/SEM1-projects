import { useState } from "react";
import axios from "axios";
import "./Modale.css";
import Swal from 'sweetalert2';

const API_URL = "http://172.17.48.124:8000/";

const SignUp = (props) => {
  const [enteredUsername, setUsername] = useState("");
  const [enteredEmail, setEmail] = useState("");
  const [enteredPassword, setPassword] = useState("");
  const [passwordType, setPasswordType] = useState("password");
  const [enteredName, setName] = useState("");
  const [enterRePass, setRePass] = useState("");

  const UserChangeHandler = (event) => {
    setUsername(event.target.value);
  };
  const NameChangeHandler = (event) => {
    setName(event.target.value);
  };

  const EmailChangeHandler = (event) => {
    setEmail(event.target.value);
  };

  const PasswordChangeHandler = (event) => {
    setPassword(event.target.value);
  };

  const togglePassword = (event) => {
    event.preventDefault();
    if (passwordType === "password") {
      setPasswordType("text");
      return;
    }
    setPasswordType("password");
  };

  const RePassChangeHandler = (event) => {
    setRePass(event.target.value);
  };

  const SignUpEnter = (event) => {
    event.preventDefault();

    const userInfo = {
      name: enteredName,
      UserName: enteredUsername,
      email: enteredEmail,
      password: enteredPassword,
      repassword: enterRePass,
    };
    axios.post(API_URL + "users", {
      username: enteredUsername,
      name: enteredName,
      email: enteredEmail,
      password: enteredPassword,
    }).then((response) => {
      console.log(response);
      //return response.data;
    }).catch(function (error) {
      if (error.response) {
        if (error.response.status == 500) {
          Swal.fire(
            'SignUp Failure!',
            'Kindly check your connectivity.',
            'error'
          )
        }
        // Request made and server responded
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      }
      // else if (error.request) {
      //   // The request was made but no response was received
      //   console.log(error.request);
      // } else {
      //   // Something happened in setting up the request that triggered an Error
      //   console.log('Error', error.message);
      // }

    });
    console.log(userInfo);
    setEmail("");
    setUsername("");
    setPassword("");
  };

  return (
    <form>
      <div class="modal" onClick={props.onClose}>
        <div class="modal-content" onClick={(e) => e.stopPropagation()}>
          <div class="modal-header">
            <div
              class="modal-title"
              onClick={() => {
                props.setShowLogin(true);
                props.setShowSignUp(false);
              }}
            >
              <h4>Login</h4>
            </div>
            <div
              class="modal-title"
              onClick={() => {
                props.setShowLogin(false);
                props.setShowSignUp(true);
              }}
            >
              <h4>Register</h4>
            </div>
          </div>

          <div className="outer-form2">
            <div className="form-content">
              <label className="left-form-content">Name</label>
              <input
                className="left-form-content2 form-control"
                type="text"
                onChange={NameChangeHandler}
                value={enteredName}
                placeholder="Name"
              />
            </div>
            <div className="form-content">
              <label className="left-form-content">Username</label>
              <input
                className="left-form-content2 form-control"
                type="text"
                onChange={UserChangeHandler}
                value={enteredUsername}
                placeholder="Username"
              />
            </div>
            <div className="form-content">
              <label className="left-form-content">Email</label>
              <input
                className="left-form-content2 form-control"
                type="text"
                onChange={EmailChangeHandler}
                value={enteredEmail}
                placeholder="Email"
              />
            </div>
            <div className="form-content">
              <label className="left-form-content">Password</label>

              <input
                type={passwordType}
                onChange={PasswordChangeHandler}
                value={enteredPassword}
                name="password"
                class="left-form-content2 form-control"
                placeholder="Password"
              />

              {/* <button
                className="btn btn-outline-primary"
                onClick={togglePassword}
              >
                {passwordType === "password" ? (
                  <i className="bi bi-eye-slash"></i>
                ) : (
                  <i className="bi bi-eye"></i>
                )}
              </button> */}
            </div>

            <div className="form-content">
              <label className="left-form-content">Reenter Password</label>

              <input
                type={passwordType}
                onChange={RePassChangeHandler}
                value={enterRePass}
                name="password"
                class="left-form-content2 form-control"
                placeholder="Password"
              />
              {/* <div className="input-group-btn">
                  <button
                    className="btn btn-outline-primary"
                    onClick={togglePassword}
                  >
                    {passwordType === "password" ? (
                      <i className="bi bi-eye-slash"></i>
                    ) : (
                      <i className="bi bi-eye"></i>
                    )}
                  </button>
                
              </div> */}
            </div>
          </div>

          <div class="footer2">
            <button onClick={SignUpEnter} class="button-33" role="button">
              Register
            </button>
          </div>
        </div>
      </div>
    </form>
  );
};
export default SignUp;
