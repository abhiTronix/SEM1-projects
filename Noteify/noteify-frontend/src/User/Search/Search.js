import { Link } from "react-router-dom";
import "../../SubjectPage/sub.css";
import SearchIcon from "@mui/icons-material/Search";
import Upload from "../Upload/Upload";

import { useState } from "react";
import SearchButton from "./SearchButton";
const Search = (props) => {
  const [showUpload, setShowUpload] = useState(false);

  var admin = JSON.parse(localStorage.getItem("admin"));

  return (
    <div>
      <div class="search">
        <div class="sub">{props.heading}</div>
        <div class="search-box">
          <button class="btn-search" onClick={() => props.handleClick()}>
            <SearchIcon fontSize="large" />
          </button>
          <input
            type="text"
            class="input-search"
            placeholder="Type to Search..."
            onChange={(e) => props.handleInputChange(e)}
          />
        </div>

      </div>

      <div class="subtop">
        <SearchButton admin={admin} setShowUpload={setShowUpload} />
      </div>
      <div>
        <Upload
          showUpload={showUpload}
          heading={props.heading}
          subjectidd={props.subjectidd}
          onClose={() => setShowUpload(false)}
        />
      </div>
    </div>
  );
};
export default Search;
