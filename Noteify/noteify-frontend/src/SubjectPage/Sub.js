import React, { useState, useEffect } from "react";
import "./sub.css";
import { useLocation } from "react-router-dom";

import Search from "../User/Search/Search.js";
import ImgDisp from "../User/ImageDisp/ImgDisp";
import DocCard from "./DocCard";
import Navigation from "./../Navigation";

const Sub = () => {
  const location = useLocation();
  const subjectid = location.state?.subjecttid;
  const name = location.state?.details;

  const filedetail = location.state?.filedetail;
  const [showDetails, setDetails] = useState(false);
  const [doc, setdoc] = useState("");
  const [subidd, subname] = subjectid.split("_");
  const [del, setdel] = useState(false);

  const [newfile, setnewfile] = useState("");
  var user = JSON.parse(localStorage.getItem("user"));
  const [searchField, setsearchField] = useState("");

  useEffect(() => {
    fetch("http://172.17.48.124:8000/data/revisions/" + name + "]_[" + subidd, {
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
      .then((data) => {
        setdoc(data);
        console.log(doc);
      });
  }, []);
  const extra = (val, it) => {
    console.log(val);
    setDetails(val);
    setnewfile(it);
  };

  const handleClick = () => { };

  const handleInputChange = (e) => {
    setsearchField(e.target.value);
    console.log(searchField);
  };
  return (
    <div>
      <Navigation />
      {!showDetails ? (
        <Search
          heading={name}
          subjectidd={subidd}
          setdel={setdel}
          handleInputChange={handleInputChange}
          handleClick={handleClick}
        />
      ) : null}


      <div class="main">
        <div className={`subject-area ${showDetails ? "subject-area2" : ""}`}>
          <DocCard
            showDetails={showDetails}
            doc={doc}
            extra={extra}
            del={del}
            searchField={searchField}
          />
        </div>
        <div class={`disp ${showDetails ? "disp2" : ""}`}>
          {showDetails ? (
            <ImgDisp extra={extra} newfile={newfile} filedetail={filedetail} user={name} />
          ) : null}
        </div>
      </div>
    </div>
  );
};
export default Sub;
