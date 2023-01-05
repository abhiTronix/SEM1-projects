import { useState } from "react";
import "./sub.css";
import { Checkbox } from "@mui/material";
const DocCard = (props) => {
  const val = Object.values(props.doc);

  //const val = ["Doc1", "Doc2", "Doc3"];
  var array = new Array();
  if (props.searchField) {
    const card = val.map((item, i) => {
      const [fname, extention] = item.split(".");
      if (props.searchField.toLocaleLowerCase() === fname.toLocaleLowerCase()) {
        return (
          <div
            className={`subject-box ${
              props.showDetails ? "subject-box2 sb2" : ""
            }`}
          >
            <div onClick={() => props.extra(true, item)} class="text">
              {item}
            </div>
          </div>
        );
      }
    });
    return card;
  } else {
    const card = val.map((item, i) => {
      return (
        <div
          className={`subject-box ${
            props.showDetails ? "subject-box2 sb2" : ""
          }`}
        >
          <div onClick={() => props.extra(true, item)} class="text">
            {item}
          </div>
        </div>
      );
    });
    return card;
  }
};
export default DocCard;
