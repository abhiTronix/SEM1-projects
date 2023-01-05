import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import "./User.css";

import SearchIcon from "@mui/icons-material/Search";
import Swal from 'sweetalert2';
import SubCard from "./Search/SubCard.js";
import Navigation from "../Navigation";

const User = () => {
  var user = JSON.parse(localStorage.getItem("user"));
  var bearer = "Bearer " + user.access_token;
  const [data1, setdata] = useState("");

  useEffect(() => {
    fetch("http://172.17.48.124:8000/posts/subcodes", {
      method: "GET",
      body: JSON.stringify(),
      headers: {
        "Content-Type": "application/json",
        Authorization: bearer,
      },
    })
      .then((response) => {
        if (!response.ok) {
          // make the promise be rejected if we didn't get a 2xx response
          throw new Error("Not 2xx response", { cause: response });
        } else {
          return response.json();
        }
      })
      .then((data) => {
        console.log(data1);
        setdata(data);
      })
      .catch((response) => {
        Swal.fire(
          'Session Expired!',
          'Kindly login again.',
          'error'
        )

      });
  }, []);

  return (
    <div>
      <Navigation />
      <div class="search">
        <div class="sub">Choose Your Subject</div>

        <div class="search-box">
          <button class="btn-search">
            <SearchIcon fontSize="large" />
          </button>

          <input
            type="text"
            class="input-search"
            placeholder="Type to Search..."
          />
        </div>
      </div>
      <div class="subject-area">
        <SubCard data={data1} />
      </div>
    </div>
  );
};
export default User;
