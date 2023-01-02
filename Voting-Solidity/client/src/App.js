import React, { useState, useEffect } from "react";
import ElectionContract from "./contracts/Election.json";
import getWeb3 from "./getWeb3";
import RegisterForm from "./components/RegisterForm";
import VoteNow from "./components/VoteNow";

import SideBar from "./components/SideBar";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import TimeLeft from "./components/TimeLeft";
import Spinner from "./components/Spinner";
import Results from "./components/Results";
import Home from "./components/Home";
import Cand from "./components/Cand";

const App = () => {
  const [loading, setLoading] = useState(true);
  const [web3, setWeb3] = useState(undefined);
  const [accounts, setAccounts] = useState([]);
  const [contract, setContract] = useState(undefined);
  const [registered, setRegistered] = useState(false);
  //const [candregistered, setcandregistered] = useState(false);
  const [voted, setVoted] = useState(false);
  const [isadmin, setIsAdmin] = useState(false);
  const [elestarted, setelestarted] = useState(false);
  const [voterdetails, setVoterdetails] = useState({
    metamaskID: "",
    name: "",
    voted: " ",
    registered: " ",
  });
  // const [canddetails, setCanddetails] = useState({
  //   candidatename: "",
  //   partyname: " ",
  //   registered: " ",
  // });
  const [starttime, setStarttime] = useState("");
  const [endtime, setEndtime] = useState("");

  const starte = async(e)=>{
    const CandidatesCount = await contract.methods
          .getCandidatesCount()
          .call(function (error, result) {
            if (!error) {
              return result;
            }
            else{
              alert("Something is wrong.");
            }
          });
    if(CandidatesCount<2){
      alert("Not enough candidates yet.");
      return;
    }
    // process to add the voter to pool.
    await contract.methods.startElection("Something EVM").send({ from: accounts[0] });
    // extract startTime and endTime from the contract specified.
    const startTime = await contract.methods
    .startTime()
    .call(function (error, result) {
      if (!error) {
        return result;
      }
    });

  const endTime = await contract.methods
    .endTime()
    .call(function (error, result) {
      if (!error) {
        return result;
      }
    });

  setStarttime(startTime);
  setEndtime(endTime);
  setelestarted(true);
  console.log("success");

  }

  useEffect(() => {
    const init = async () => {
      try {
        // load web3.
        const web3 = await getWeb3();
        // get the Metamask account.
        const accounts = await web3.eth.getAccounts();
        // get the network id.
        const networkId = await web3.eth.net.getId();
        // get the contract deployed on the network(particularly on definite network id).
        const deployedNetwork = ElectionContract.networks[networkId];
        //  Create an instance of your contract.
        const instance = new web3.eth.Contract(
          ElectionContract.abi,
          deployedNetwork && deployedNetwork.address
        );

        // set web3, accounts, contract instance.
        setWeb3(web3);
        setAccounts(accounts);
        setContract(instance);

        const started = await instance.methods
          .electionstarted()
          .call();
        setelestarted(started);

        // extract voterDetails.
        const voterInstance = await instance.methods
          .voters(accounts[0])
          .call(function (err, result) {
            if (!err) {
              return result;
            }
          });
        const hasRegistered = voterInstance[3];

        // const candInstance = await instance.methods
        //   .candidates(1)
        //   .call(function (err, result) {
        //     if (!err) {
        //       return result;
        //     }
        //   });
        // const hasRegisteredCand = candInstance[2];

        // setCanddetails({
        //   candidatename: candInstance[0],
        //   partyname: candInstance[1],
        //   registered: candInstance[2],
        // });

        setVoterdetails({
          metamaskID: voterInstance[0],
          name: voterInstance[1],
          voted: voterInstance[2],
          registered: voterInstance[3],
        });

        setRegistered(hasRegistered);
        //setcandregistered(hasRegisteredCand);

        setVoted(voterInstance[2]);

        // extract startTime and endTime from the contract specified.
        const startTime = await instance.methods
          .startTime()
          .call(function (error, result) {
            if (!error) {
              return result;
            }
          });

        const endTime = await instance.methods
          .endTime()
          .call(function (error, result) {
            if (!error) {
              return result;
            }
          });

        const checkadmin = await instance.methods
          .isadmin()
          .call();

        setIsAdmin(checkadmin);
        setStarttime(startTime);
        setEndtime(endTime);
        setLoading(false);
      } catch (error) {
        console.error(error);
        console.log("something is wrong");
        // alert(
        //   `Failed to load web3, accounts, or contract. Check console for details.`
        // );
        
      }
    };
    init();
  }, [
    web3,
    accounts,
    contract,
    registered,
    voterdetails,
    loading,
    voted,
    starttime,
    endtime,
  ]);

  return (
    <div>
      <Router>
        <SideBar starte={starte} elestarted={elestarted}/>
        <div className="content">
          <div className="center-elements">
            {loading ? (
              <Spinner />
            ) : (
              <>
                <Routes>
                  <Route exact path="/" element={<Home />}></Route>
                  <Route
                    exact
                    path="/register"
                    element={
                      <RegisterForm
                        setVoterdetails={setVoterdetails}
                        setRegistered={setRegistered}
                        registered={registered}
                        voterdetails={voterdetails}
                        contract={contract}
                        accounts={accounts}
                        web3={web3}
                      />
                    }
                  ></Route>
                  <Route
                    exact
                    path="/voteNow"
                    element={
                      <VoteNow
                        setVoterdetails={setVoterdetails}
                        setVoted={setVoted}
                        contract={contract}
                        registered={registered}
                        voterdetails={voterdetails}
                        voted={voted}
                        accounts={accounts}
                        web3={web3}
                      />
                    }
                  ></Route>
                  <Route
                    exact
                    path="/candidate"
                    element={
                      <Cand  
                      contract={contract}
                      accounts={accounts}
                      web3={web3}
                      elestarted={elestarted}
                       />
                      
                    }
                  ></Route>
                  <Route
                    exact
                    path="/results"
                    element={
                      <Results
                        contract={contract}
                        accounts={accounts}
                        web3={web3}
                      />
                    }
                  ></Route>
                </Routes>
              </>
            )}
          </div>
          {loading ? (
            "loading..."
          ) : (
            <TimeLeft
              contract={contract}
              accounts={accounts}
              starttime={starttime}
              endtime={endtime}
            />
          )}
        </div>
      </Router>
    </div>
  );
};

export default App;
