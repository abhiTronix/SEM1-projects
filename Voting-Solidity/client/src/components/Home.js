import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";

const Home = () => {
  return (
    <div className="body-content">
      <h1>
        Welcome to <br></br>Decentralized Voting App{" "}
      </h1>

      <div className="body-text-content">
        <ol>
          <li className="parah">
            Register into the app during a limited registration phase. This
            registration phase is started by election administrators. If the
            period of time is missed, you cannot be verified and therefore
            cannot cast your vote in the current session. You can register{" "}
            <Link color="red" to="/register">
              HERE
            </Link>{" "}
            during the announced time period.
          </li>
          <li className="parah">
            You can see the progress of your verification request on the same
            page you have used to register. Your personal data, such as name are
            encrypted and can only be decrypted by an administrator.
          </li>
          <li className="parah">
            Once you have been approved, you can consult the list of parties and
            other related data
            <Link to="/result"> HERE</Link>. Every party has a{" "}
            <i>unique name</i> used for casting the vote.
          </li>
          <li className="parah">
            You can cast your vote <Link to="/voteNow">HERE</Link> but only
            after registering. The Administrator is responsible for starting and
            ending a voting session. You can only cast a vote for a party in the
            announced time period. A list of parties from your constituency is
            available on the voting page. You can only cast your vote once by
            clicking the unique name of your preffered party.
          </li>
          <li className="parah">
            After the election has ended, the you can visualize the results
            publicly.
          </li>
        </ol>
      </div>
    </div>
  );
};

export default Home;
