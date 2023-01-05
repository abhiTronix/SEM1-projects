import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import "./../../User/User.css";
import Navigation from "./../../Navigation";
import SearchIcon from "@mui/icons-material/Search";
import Swal from 'sweetalert2';
import FileCard from "./FileCard";
import SearchButton from "./../Search/SearchButton";
import Upload from "../Upload/Upload";

const User = (props) => {
  const location = useLocation();
  var admin = JSON.parse(localStorage.getItem("admin"));

  const subjectname = location.state?.details;
  var user = JSON.parse(localStorage.getItem("user"));
  var bearer = "Bearer " + user.access_token;
  const [filename, setfilename] = useState("");
  const [filedetail, setfiledetail] = useState();

  useEffect(() => {
    fetch(
      "http://172.17.48.124:8000/data/versions/" + subjectname,

      {
        method: "GET",
        body: JSON.stringify(),
        headers: {
          "Content-Type": "application/json",
          Authorization: bearer,
        },
      }
    )
      .then((response) => {
        if (!response.ok) {
          // make the promise be rejected if we didn't get a 2xx response
          throw new Error("Not 2xx response", { cause: response });
        } else {
          return response.json();
        }
      })
      .then((data) => {
        setfilename(data);
        console.log(data);
      })
      .catch((response) => {
        Swal.fire(
          'No posts!',
          'Apologies, Posts not there yet.',
          'error'
        )

      });
  }, []);

  useEffect(() => {
    fetch(
      "http://172.17.48.124:8000/posts/find/" + subjectname,

      {
        method: "GET",
        body: JSON.stringify(),
        headers: {
          "Content-Type": "application/json",
          Authorization: bearer,
        },
      }
    )
      .then((response) => {
        if (!response.ok) {
          // make the promise be rejected if we didn't get a 2xx response
          throw new Error("Not 2xx response", { cause: response });
        } else {
          return response.json();
        }
      })
      .then((data1) => {
        setfiledetail(data1);
        console.log(filedetail);
      }).catch((response) => {
        Swal.fire(
          'No posts!',
          'Apologies, Posts not there yet.',
          'error'
        )

      });
  }, []);
  const [showUpload, setShowUpload] = useState(false);
  const [subid, subname] = subjectname.split("_");

  return (
    <div>
      <Navigation />
      <div class="search">
        <div class="sub">{subname} : {subid}</div>

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
      <div class="subtop">
        <SearchButton admin={admin} setShowUpload={setShowUpload} />
      </div>
      <div>
        <Upload
          showUpload={showUpload}
          heading={user.username}
          subjectidd={subid}
          onClose={() => setShowUpload(false)}
        />
      </div>
      <div class="subject-area">
        <FileCard
          data={filename}
          subjectname={subjectname}
          filedetail={filedetail}
        />
      </div>
    </div>
  );
};
export default User;
