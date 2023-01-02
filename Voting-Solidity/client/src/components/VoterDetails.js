import React from 'react';
import '../App.css';

/* Function to display voter's details;
 its MetaMask ID, Name, whether registered or not , whether voted or not */
const VoterDetails = (props) => {
  return (
    <div>

      <div className='voterDetails'>
        <div className='word'>Voter Details</div>
        <table className="table">
          <thead>
          </thead>
          <tbody style={{ color: '#f2f2fa' }}>
            <tr>
              <th scope="row">Metamask ID</th>
              <td>{props.voterdetails.metamaskID}</td>
            </tr>
            <tr>
              <th scope="row">Name</th>
              <td>{props.voterdetails.name}</td>

            </tr>
            <tr>
              <th scope="row">Registered</th>
              <td colSpan="2">
                {props.voterdetails.registered ? 'Yes' : 'No'}
              </td>

            </tr>
            <tr>
              <th scope="row">Voted</th>
              <td colSpan="2">{props.voterdetails.voted ? 'Yes' : 'No'}</td>

            </tr>
          </tbody>
        </table>
      </div>
    </div>

  )
}

export default VoterDetails