import { Link } from "react-router-dom";
import "./../../User/User.css";
const SubCard = (props) => {
  const val = Object.values(props.data);

  //const val = ["CS123", "CS468", "CS569"];
  const card = val.map((item, i) => {
    const [subid, subname] = item.split("_");
    console.log(subid, subname);
    return (
      <Link to="/user/file" className="box" state={{ details: item }}>
        <div>
          <div class="text">
            <h class="sub-text">{subname}</h> : {subid}
          </div>
        </div>
      </Link>
    );
  });
  return card;
};
export default SubCard;
