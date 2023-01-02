import React, { useRef, useState } from "react";
import "../App.css";
import VoterDetails from "./VoterDetails";
import { useNavigate } from "react-router-dom";
import Spinner from "./Spinner";

const RegisterForm = (props) => {
  const [loading, setLoading] = useState(false);
  const nameOfVoter = useRef(null);
  const [name, setName] = useState("");
  let navigate = useNavigate();

  // function to set voter's name.
  // Note: Other details such as voter id(i.e metamask id in this case) will be directly extracted.

  const onChange = (e) => {
    setName({ ...name, [e.target.name]: e.target.value });
  };

  // function to add the voter to the pool(i.e decentralized database).
  const addVoter = async () => {
    setLoading(true);

    const contract = props.contract;
    const accounts = props.accounts;

    // get the name of the voter from the input field.
    const form = nameOfVoter.current;
    let vname = form["name"].value;

    // process to add the voter to pool.
    await contract.methods.addVoter(vname).send({ from: accounts[0] });

    props.setRegistered(true);

    // reset the voterVoterdetails.
    props.setVoterdetails({
      metamaskID: accounts,
      name: vname,
      voted: false,
      registered: true,
    });

    // Loading completed.
    setLoading(false);

    // navigate to voteNow as soon the registration process is complete.
    navigate("/voteNow", { replace: true });
  };

  return (
    <div>
      {loading ? (
        <Spinner />
      ) : (
        <>
          {props.registered ? (
            <VoterDetails voterdetails={props.voterdetails} />
          ) : (
            <div className="reg">
              <div className="registerText">Register yourself:</div>
              <div
                className="btn-group"
                role="group"
                aria-label="Basic example"
              >
                <form ref={nameOfVoter}>
                  <input
                    type="text"
                    className="form-control"
                    aria-label="name"
                    name="name"
                    placeholder="Rahul Parkar"
                    onChange={onChange}
                  />
                </form>

                <button
                  type="button"
                  className="btn btn-primary"
                  disabled={name.length < 3}
                  onClick={addVoter}
                >
                  Register
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default RegisterForm;
