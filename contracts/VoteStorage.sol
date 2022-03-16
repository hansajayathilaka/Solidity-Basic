// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;


contract VoteStorage {

    address public owner;

    mapping(string => uint256[]) votes;
    mapping(uint256 => uint256) results;
    string[] voters;
    uint256[] public competitors;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner, "Permission denied.");
        _;
    }

    function create_vote(string memory user_hash, uint256 competitor_index) public onlyOwner {
        if (votes[user_hash].length > 0) {
            for(uint256 i = 0; i < votes[user_hash].length; i++) {
                require(votes[user_hash][i] != competitor_index, "This vote is duplicated.");
            }
        } else {
            voters.push(user_hash);
        }

        bool found = false;
        for(uint256 i = 0; i < competitors.length; i++) {
            if (competitors[i] == competitor_index) {
                found = true;
                break;
            }
        }
        if (found == false) {
            competitors.push(competitor_index);
        }

        votes[user_hash].push(competitor_index);
        results[competitor_index]++;
    }

    function voters_count() public view returns(uint256) {
        return voters.length;
    }

    function get_result(uint256 user_hash) public view returns(uint256) {
        return results[user_hash];
    }
}
