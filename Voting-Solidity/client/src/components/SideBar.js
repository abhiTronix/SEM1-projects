import React from "react";
import "../App.css";
import { Link } from "react-router-dom";
import image from "./images/image_website_blockchain_app.jpg";

const SideBar = (props) => {
  return (
    <div>
      <div className="sidebar">
        <div className="sidebarContent">
          <Link to="/" className="sidebarText">
            <i className="fas fa-home"></i> <span>Home</span>
          </Link>
          {(!props.elestarted)&&<Link to="/candidate" className="sidebarText">
            <i className="fas fa-home"></i> <span>Administrator</span>
          </Link>}
          
          
          {(props.elestarted)&&<Link to="/register" className="sidebarText text-center">
            <span>Voter Registration</span>
          </Link>}
          {(props.elestarted)&&<Link to="/voteNow" className="sidebarText text-center">
            <span>Vote Now</span>
          </Link>}
        </div>
        {(!props.elestarted)&&<button class="button-82-pushable" role="button" onClick={()=>props.starte()}>
            <span class="button-82-shadow"></span>
            <span class="button-82-edge"></span>
            <span class="button-82-front text">
            Start Elections
            </span>
          </button>}
      </div>
    </div>
  );
};

export default SideBar;
