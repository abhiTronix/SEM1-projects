import React from "react";
import { Link } from "react-router-dom";
import Navigation from "../Navigation";
import "./Main.css";
import "./../"
import Swal from 'sweetalert2';
import { useNavigate } from "react-router-dom";

const Main = () => {
  var user_val = "";
  if (localStorage.getItem("user") != null) {
    user_val = JSON.parse(localStorage.getItem("user"));
  }
  let navigate = useNavigate();
  async function check(props) {
    fetch("http://172.17.48.124:8000/data/status/" + user_val.username, {
      method: "GET",
      body: JSON.stringify(),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        //console.log(response);
        return response.json();
      })
      .then((user) => {
        console.log(user);
        if (!user_val || !user) {
          Swal.fire(
            'Login?',
            'Kindly login first!',
            'error'
          )
        }
        else {
          navigate('/user');
        }
      });
  }
  return (
    <div>
      <Navigation />
      <div className="heading">
        <div class="head">Noteify</div>

        <div class="tag-line"> Notes sharing made easier </div>

        <div class="startbut">
          <button class="button-49" role="button" onClick={check}>
            Get Started
          </button>
        </div>
      </div>
      <div class="heading2"></div>
    </div>
  );
};

export default Main;
