import React, { useState, useEffect } from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Modale from "./Modal/Modale";
import AdminModale from "./Admin/Modal/AdminModale";
import Swal from 'sweetalert2';
import { useNavigate } from "react-router-dom";

const Navigation = () => {
  const [show, setShow] = useState(false);
  const [show1, setShow1] = useState(false);
  const MINUTE_MS = 300000;
  var user_val = "";
  var admin = false;
  if (localStorage.getItem("user") != null) {
    user_val = JSON.parse(localStorage.getItem("user"));
  }
  if (localStorage.getItem("admin") != null) {
    admin = JSON.parse(localStorage?.getItem("admin"));
  }
  const [user, setuser] = useState("");
  let navigate = useNavigate();

  const logout = () => {
    var bearer = "Bearer " + user_val.access_token;
    if (user && admin === true) {
      fetch("http://172.17.48.124:8000/mods/logout", {
        method: "POST",
        body: JSON.stringify(),
        headers: {
          "Content-Type": "application/json",
          Authorization: bearer,
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          console.log(data);
          localStorage.removeItem("user");
          localStorage.removeItem("admin");
          navigate('/');
          window.location.reload();
        });
    }
    else if (user) {
      fetch("http://172.17.48.124:8000/logout", {
        method: "POST",
        body: JSON.stringify(),
        headers: {
          "Content-Type": "application/json",
          Authorization: bearer,
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          console.log(data);
          localStorage.removeItem("user");
          localStorage.removeItem("admin");
          navigate('/');
          window.location.reload();

        });
    }
    else {
      console.log("Login First")
    }
  };

  useEffect(() => {
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
        setuser(user);
        console.log(user);
      });
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      console.log('Logs every minute');
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
          if (user === false) {
            Swal.fire(
              'Session Expired!',
              'Kindly login again.',
              'error'
            )
            navigate('/');
          }
        });
    }, MINUTE_MS);

    return () => clearInterval(interval); // This represents the unmount function, in which you need to clear your interval to prevent memory leaks.
  }, [])

  if (!user) {
    return (
      <div class="navcontainer">
        <button class="button-10" onClick={() => setShow(true)}>
          Login
        </button>

        <button
          class="btn but btn-outline-primary"
          onClick={() => setShow1(true)}
        >
          Moderator Login
        </button>
        <Modale show={show} onClose={() => setShow(false)} />
        <AdminModale show={show1} onClose={() => setShow1(false)} />
      </div>
    );
  } else {
    return (
      <div class="navcontainer">
        <div className="username"> Hey {user_val.username}</div>
        <button class="button-10" onClick={() => logout()}>
          Logout
        </button>
      </div>
    );
  }
};

export default Navigation;
