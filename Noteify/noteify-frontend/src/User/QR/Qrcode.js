import "./Qrcode.css";
import { useState } from "react";

const Qrcode = (props) => {
  if (!props.show) {
    return null;
  } else {
    return (
      <div className="modall" onClick={props.onClose}>
        <div class="modall-content" onClick={(e) => e.stopPropagation()}>
          <img
            src={
              "http://172.17.48.124:8000/data/qr/" +
              encodeURIComponent(props.filename)
            }
          />
        </div>
      </div>
    );
  }
};
export default Qrcode;
