import React, { useState, useEffect } from 'react';
import '../App.css';
import RegisterForm from './RegisterForm';
import VoterDetails from './VoterDetails';
import Spinner from './Spinner';

const VoteNow = (props) => {

    const [loading, setLoading] = useState(true);
    const [getCandidates, setgetCandidates] = useState([]);
    const { contract, accounts, voterdetails, setVoterdetails, voted, setVoted } = props;

    useEffect(() => {

        const loadEssentials = async () => {

            // extracting all the candidates from the contract stored.
            const candidates_count = await contract.methods.getCandidatesCount().call();

            console.log(candidates_count);

            setVoted(voted);
            let candidatesObj_1 = [];
            for (let i = 0; i < candidates_count; i++) {
                let j = i + 1;

                // extracting all the candidates from the contract stored.
                const candidates = await contract.methods.getCandidateByID(j).call();

                console.log(candidates);

                // setting candidates id and name for every candidate in the pool.
                candidatesObj_1[i] = { candidatename: candidates[0], partyname: candidates[1], candidateID: j }
            }
            setgetCandidates(candidatesObj_1);
            console.log("test");
            console.log(getCandidates);
            setLoading(false);

        }
        loadEssentials();

    }, [loading, setVoted, contract, voted]);

    const castVote = async (idNum) => {

        // catching the value sent on button click.
        let id = idNum.target.value;

        // vote casting process.
        /* making changes in the contrac's ledger,
         which will act as database( like in centralized database). */
        await contract.methods.vote(id).send({ from: accounts[0] });
        console.log('success');
        setVoted(true);

        // reset all the details including voted or not
        setVoterdetails({ metamaskID: voterdetails.metamaskID, name: voterdetails.name, voted: true, registered: true })

    }


    return (
        <div>
            {loading ?
                <Spinner /> :
                <>
                    {/* If voter has registered and not voted. */}
                    {props.registered && !voted ?
                        <div className='candidateDetails'>
                            <div className='word'>Candidates</div>
                            <table className="table">
                                <thead>
                                </thead>
                                <tbody style={{ color: 'white' }}>
                                    {/* print all the candidates. */}
                                    {getCandidates.map(party => (
                                        <tr key={party.candidateID}>
                                            <th scope="row">{party.candidatename}({party.partyname})</th>
                                            <td><button type="button" className="btn btn-warning text-danger" value={party.candidateID} onClick={castVote}>VOTE</button></td>
                                        </tr>
                                    ))}

                                </tbody>
                            </table>
                        </div>
                        :
                        <>
                            {/* if voter has voted and also is registered account. */}
                            {voted && props.registered ?
                                <VoterDetails voterdetails={voterdetails} />
                                :
                                // If above conditions not met then show REGISTRATION PAGE.
                                <RegisterForm />
                            }
                        </>

                    }
                </>

            }
        </div>


    )
}

export default VoteNow