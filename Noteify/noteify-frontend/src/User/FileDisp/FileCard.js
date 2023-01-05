import { Link } from "react-router-dom";
import "./../../User/User.css";
const FileCard = (props) => {
  const val = Object.values(props.data);

  //const val = ["@san", "@surajpammi"];
  const card = val.map((item, i) => {
    return (
      <Link
        to="/user/file/sub"
        className="box"
        state={{
          details: item,
          subjecttid: props.subjectname,
          filedetail: props.filedetail,
        }}
      >
        <div>
          <div class="text">
            <h class="sub-text">{item}</h>
          </div>
        </div>
      </Link>
    );
  });
  return card;
};
export default FileCard;
