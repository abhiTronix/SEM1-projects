import React, { useState, useEffect } from 'react';
import BJP from './images/BJP.png';
import Congress from './images/Congress.png';
import AAP from './images/AAP.png';
import NCP from './images/NCP.png';
import Spinner from './Spinner';

const Results = (props) => {

  const [candidateDetails, setcandidateDetails] = useState([]);
  const [tieChecker, settieChecker] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    const candidates_And_Votes = async () => {

      // storing all the candidates except winner(s).
      let candidatesObj = [];
      // storing winner(s) details.
      let candidatesPlace1 = [];

      // get the winning candidate from the smart contract.
      const foundWinner = await props.contract.methods.getWinningCandidate().call();
      // extracting all the candidates from the contract stored.
      const candidates_count = await props.contract.methods.getCandidatesCount().call();
      for (let i = 1; i <= candidates_count; i++) {
        let j = i - 1;

        // get all candidates details.
        let candidates = await props.contract.methods.getVoteCountFor(i).call();

        // extracting all the candidates from the contract stored.
        const candidate = await props.contract.methods.getCandidateByID(i).call();

        // check for the tie, if the other candidates in the pool has similar number of votes.
        // vote count for each candidate being compared with the winners voteCount.
        if (candidates[0] === foundWinner[2]) {
          candidatesPlace1[j] = {
            name: candidates[1],
            partyname: candidate[1],
            votes: candidates[0]
          };
        } else {
          candidatesObj[j] = {
            name: candidates[1],
            partyname: candidate[1],
            votes: candidates[0]
          };
        }

      }

      // removing the null, undefined or empty objects if present any, in the array.
      candidatesObj = candidatesObj.filter(function (el) {
        return el !== null;
      })

      candidatesPlace1 = candidatesPlace1.filter(function (el) {
        return el !== null;
      })

      // storing candidate's details, except for the winner(s).
      setcandidateDetails(candidatesObj);
      // storing winner(s) details.
      settieChecker(candidatesPlace1);
      setLoading(false)

    }

    candidates_And_Votes();

  }, [props])


  return (

    <>
      {loading ?
        <Spinner /> :
        <>
          <div className="container-fluid">
            <div className="row">

              {/* display all the winner(s) */}
              {tieChecker.map(winners => (
                <div key={winners.name} className={`col py-2 my-2 d-flex justify-content-center`}>
                  <>
                    <div className='px-1'>
                      <div className='results card' style={{ width: "13rem" }}>
                        {winners.partyname === "Congress" ?
                          <img src={Congress} width={"90px"} height={'200px'} className="card-img-top" alt="..." />
                          :
                          <>
                            {winners.partyname === "BJP" ?
                              <img src={BJP} width={"90px"} height={'200px'} className="card-img-top" alt="..." />
                              :
                              <>
                                {winners.partyname === "AAP" ?
                                  <img src={AAP} width={"90px"} height={'200px'} className="card-img-top" alt="..." />
                                  :
                                  <img src={NCP} width={"90px"} height={'200px'} className="card-img-top" alt="..." />
                                }
                              </>
                            }
                          </>
                        }

                        <div className='card-body'>
                          <h5 className="card-title text-center">{winners.name}</h5>
                          <p className='card-text text-center'>Votes Received : {winners.votes}</p>
                        </div>

                        <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-warning" style={{ zIndex: "5" }}>
                          {tieChecker.length === 1 ? "WINNER" : "TIE"}
                        </span>

                      </div>
                    </div>
                  </>
                </div>

              ))}

            </div>
            <div className="row">

              {/* display all the other candidates except winner(s) */}
              {candidateDetails.map(candidate => (
                <div key={candidate.name} className='col py-4 d-flex justify-content-center'>
                  <>
                    <div className='px-1'>
                      <div className='results card' style={{ width: "13rem" }}>

                        <div className='card-body'>
                          <h5 className="card-title text-center">{candidate.name} </h5>
                          <p className='card-text'>Votes Received: {candidate.votes}</p>
                        </div>
                      </div>
                    </div>
                  </>
                </div>
              ))}

            </div>
          </div>
        </>}
    </>
  )
}

export default Results