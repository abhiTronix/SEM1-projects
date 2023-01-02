import "./Cand.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import React, { useEffect, useState } from "react";

const Cand = (props) => {
  const [loading, setLoading] = useState(false);
  const [name, setname] = useState("");
  const [partyname, setpartyname] = useState("BJP");
  const [regcount, setregcount] = useState(0);
  const [partystatus, setpartystatus] = useState({
    BJP: false,
    Congress: false,
    AAP: false,
    NCP:false,
  });
  const [canddetails, setCanddetails] = useState({
      candidatename: "",
      partyname: " ",
      registered: false,
    });
  const [candregistered, setcandregistered] = useState(false);
  const [val, setval] = useState("");

  // function to add the voter to the pool(i.e decentralized database).
 

const handleChange1 = (e) =>{
  setname(e.target.value);
}
const handleChange2 = (e) =>{
  setpartyname(e.target.value);
}

const handleSubmit = async (e) =>{

  e.preventDefault();
  var status = partystatus;
  if (status[partyname] != true)
  {
    status[partyname] = true;
    setpartystatus(status);
  }
  else{
    alert("Party candidate already registered!")
    return;
  }
  
  setLoading(true);

    const contract = props.contract;
    const accounts = props.accounts;
    console.log(name);
    console.log(partyname);

    // process to add the voter to pool.
    await contract.methods.addCandidate(name, partyname).send({ from: accounts[0] });

    setcandregistered(true);

    // reset the voterVoterdetails.
    setCanddetails({
      candidatename: name,
      partyname: partyname,
      registered: false,
    });

    // Loading completed.
    setLoading(false);
    var count = regcount;
    setregcount(++count);
    setval("");
  console.log(name, partyname);

}
  // function to set voter's name.
  // Note: Other details such as voter id(i.e metamask id in this case) will be directly extracted.

  // function to add the voter to the pool(i.e decentralized database).

  // get the name of the voter from the input field.
  //const form = nameOfVoter.current;
  //let vname = form["name"].value;

  // process to add the voter to pool.
  // await contract.methods.addVoter(vname).send({ from: accounts[0] });

  return (
    <div>
      <h1>Candidates Registration</h1>
      <br></br>
      <div className="reg">
        
        <div className="inner">
          <Form  onSubmit={handleSubmit}> 
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Candidate Name</Form.Label>
              <Form.Control placeholder="Enter name" onChange={handleChange1}/>
            </Form.Group>
            <Form.Group className="mb-3">
        <Form.Label>Party Name</Form.Label>
        <Form.Select onChange={handleChange2}> 
          <option>BJP</option>
          <option>Congress</option>
          <option>AAP</option>
          <option>NCP</option>
        </Form.Select>
      </Form.Group>


         
            <Button  className="button-36" type="submit" disabled={props.elestarted}>
              Submit
            </Button>
            
          </Form>
          

          

        </div>
      </div>
    </div>
  );
};
export default Cand;
