// SPDX-License-Identifier: MIT

pragma solidity >=0.4.21 <0.9.0;
import "./Votes.sol";

contract Election { 
    // candidates
    address private admin;
    string public topic;
    uint256 public startTime;
    uint256 public endTime;
    uint256 private candidatesCount;
    struct Candidate {
        string candidatename;
        string partyname;
        bool registered;
    }
    struct Status{
        string candidatename;
        bool approved;
    }
    mapping(uint256 => Candidate) public candidates;
    mapping(string => Status) public candidates_registered;
    
    // voters
    uint256 public votersCount;
    struct Voter {
        address voterAddress;
        string name;
        bool voted;
        bool registered; // to check if this voter has registered
        uint256 candidateId;
    }
    mapping(uint256 => uint256) private voteCount;
    mapping(address => Voter) public voters;

    // constructor call
    constructor() public {
        admin = msg.sender;
        topic = "Unknown";
    }

    modifier adminOnly() {
        require(admin == msg.sender);
        _; //used inside a modifier to specify when the function should be executed.
    }

    modifier registeredVotersOnly() {
        require(voters[msg.sender].registered);
        _;
    }

    modifier withinTimeLimit() {
        require(block.timestamp < endTime);
        _;
    }

    modifier afterTimeLimit() {
        require(block.timestamp > endTime);
        _;
    }

    event voterRegistered(address _voterAddress);

    event candidateRegistered(address _candidateAddress);

    event voteCasted(address _voterAddress);

    event electionStarted(address _candidateAddress);

    function timestamp() external view returns (uint256) {
        return block.timestamp;
    }

    function getCandidatesCount()
        public
        view
        returns (
            uint256
        )
    {
        return (
            candidatesCount
        );
    }

    function isadmin()
        public
        view
        returns (
            bool
        )
    {
        if (admin == msg.sender){
            return true;
        }
        else {
            return false;
        }
    }

    function electionstarted()
        public
        view
        returns (
            bool
        )
    {
        if (startTime>0){
            return true;
        }
        else {
            return false;
        }
    }


    function getCurrentVoter()
        public
        view
        returns (
            address,
            string memory,
            bool,
            bool,
            uint256
        )
    {
        Voter memory voter = voters[msg.sender];
        return (
            voter.voterAddress,
            voter.name,
            voter.voted,
            voter.registered,
            voter.candidateId
        );
    }

    function getCandidateByID(uint _id)
        public
        view
        returns (
            string memory,
            string memory,
            bool
        )
    {
        require(candidates[_id].registered, "Candidate does not exist.");
        return (
            candidates[_id].candidatename,
            candidates[_id].partyname,
            candidates[_id].registered
            
        );
    }

    function addCandidate(string memory _name, string memory _party) public {
        //require(admin == msg.sender, "You're not the admin");
        require(bytes(_name).length>0, "Name is required.");
        require(bytes(_party).length>0, "Party name is required.");
        require(!candidates_registered[_party].approved, "This party already have registered candidate.");
        candidatesCount++;
        candidates[candidatesCount] = Candidate(_name, _party, true);
        candidates_registered[_party] = Status(_name, true);
        emit candidateRegistered(msg.sender);
    }

    function addVoter(string memory _name) public {
        require(bytes(_name).length>0, "Name is required.");
        require(!voters[msg.sender].registered, "You've already registered.");
        votersCount++;
        voters[msg.sender] = Voter(msg.sender, _name, false, true, 0);
        emit voterRegistered(msg.sender);
    }

    // main voting function takes your selected candidate id and increments their vote count
    function vote(uint256 _candidateId)
        public
        registeredVotersOnly
        withinTimeLimit
    {
        require(candidatesCount>1, "Not enough candidates.");
        require(!voters[msg.sender].voted);
        voteCount[_candidateId]++;
        voters[msg.sender].voted = true;
        voters[msg.sender].candidateId = _candidateId;
        emit voteCasted(msg.sender);
    }


    function startElection(string memory _topic) public {
        //require(admin == msg.sender, "You're not the admin");
        require(startTime==0, "Elections already running.");
        require(candidatesCount>1, "Not enough candidates.");
        if (bytes(_topic).length>0){
            topic = _topic;
        }
        startTime = block.timestamp;
        endTime = startTime + 5 minutes;
        emit electionStarted(msg.sender);
    }

    function getVoteCountFor(uint256 _candidateId)
        external
        view
        returns (uint256, string memory)
    {
        return (voteCount[_candidateId], candidates[_candidateId].candidatename);
    }

    // returns (id, name, voteCount) of the winning candidate
    function getWinningCandidate()
        external
        view
        returns (
            uint256,
            string memory,
            uint256
        )
    {
        uint256 maxVote = 0;
        uint256 maxVoteCandidateId = 0;
        for (uint256 i = 0; i <= candidatesCount; i++) {
            if (maxVote < voteCount[i]) {
                maxVote = voteCount[i];
                maxVoteCandidateId = i;
            }
        }
        return (
            maxVoteCandidateId,
            candidates[maxVoteCandidateId].candidatename,
            maxVote
        );
    }
}
