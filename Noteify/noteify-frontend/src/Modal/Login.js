import { useState } from "react";
import "./Modale.css";
import axios from "axios";
import Swal from 'sweetalert2';


const API_URL = "http://172.17.48.124:8000/";

const Login = (props) => {
  const [enteredUsername, setUsername] = useState("");
  const [enteredEmail, setEmail] = useState("");
  const [enteredPassword, setPassword] = useState("");
  const [passwordType, setPasswordType] = useState("password");

  const [tokenId, settokenId] = useState("");

  const UserChangeHandler = (event) => {
    setUsername(event.target.value);
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

  const LoginEnter = (event) => {
    event.preventDefault();

    const headers = {
      "Content-Type": "application/x-www-form-urlencoded",
    };
    const form = new FormData();
    form.append("username", enteredUsername);
    form.append("password", enteredPassword);
    axios
      .post(API_URL + "login", form, { timeout: 10000, headers: headers })
      .then((response) => {
        if (response.data.access_token) {
          localStorage.setItem("user", JSON.stringify(response.data));
        }
        console.log(response.data);
        //settokenId(response.data.access_token);
        localStorage.setItem("user", JSON.stringify(response.data));
        localStorage.setItem("admin", false);
        window.location.reload();

        //return response.data;
      }).catch(function (error) {
        if (error.response) {
          if (error.response.status == 400) {
            Swal.fire(
              'Login Failure!',
              'Kindly check your username and password.',
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
              class="modal-title1"
              onClick={() => {
                props.setShowLogin(true);
                props.setShowSignUp(false);
              }}
            >
              <h4>Login</h4>
            </div>
            <div
              class="modal-title2"
              onClick={() => {
                props.setShowLogin(false);
                props.setShowSignUp(true);
              }}
            >
              <h4>Register</h4>
            </div>
          </div>

          <div className="outer-form">
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
              <label className="left-form-content">Password</label>

              <input
                type={passwordType}
                onChange={PasswordChangeHandler}
                value={enteredPassword}
                name="password"
                class=" left-form-content2 form-control"
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
        </div>
        <div class="footer">
          <button onClick={LoginEnter} class="button-37" role="button">
            Login
          </button>
        </div>
      </div>
    </form>
  );
};
export default Login;
