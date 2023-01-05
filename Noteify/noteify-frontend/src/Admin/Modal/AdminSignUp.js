import { useState } from "react";
import axios from "axios";
import "./Modale.css";
import Swal from 'sweetalert2';

const API_URL = "http://172.17.48.124:8000/mods";

const AdminSignUp = (props) => {
  const [enteredUsername, setUsername] = useState("");
  const [enteredEmail, setEmail] = useState("");

  const [enteredName, setName] = useState("");

  const UserChangeHandler = (event) => {
    setUsername(event.target.value);
  };
  const NameChangeHandler = (event) => {
    setName(event.target.value);
  };

  const EmailChangeHandler = (event) => {
    setEmail(event.target.value);
  };

  const SignUpEnter = (event) => {
    event.preventDefault();

    const userInfo = {
      name: enteredName,
      UserName: enteredUsername,
      email: enteredEmail,
    };
    axios.post(API_URL, {
      username: enteredUsername,
      name: enteredName,
      email: enteredEmail,
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
              <h4>Sign Up</h4>
            </div>
          </div>

          <div className="outer-form">
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
          </div>

          <div class="footer2">
            <div class="button-33" onClick={SignUpEnter}>
              Register
            </div>
          </div>
        </div>
      </div>
    </form>
  );
};
export default AdminSignUp;
