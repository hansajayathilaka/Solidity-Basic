// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "./VoteStorage.sol";


contract DynamicVoteStorage {

    address public owner;
    VoteStorage[] public voteStorages;
    uint256 voteStorageIndex = 0;

    constructor() {
        owner = msg.sender;
        VoteStorage voteStorage =  new VoteStorage();
        voteStorages.push(voteStorage);
    }

    modifier onlyOwner {
        require(msg.sender == owner, "Permission denied.");
        _;
    }

    function create_new_event() public onlyOwner returns(address) {
        VoteStorage voteStorage =  new VoteStorage();
        voteStorages.push(voteStorage);
        voteStorageIndex++;
        return address(voteStorage);
    }

    function create_vote(string memory user_hash, uint256 competitor_index) public onlyOwner {
        VoteStorage voteStorage = VoteStorage(address(voteStorages[voteStorageIndex]));
        voteStorage.create_vote(user_hash, competitor_index);
    }

    function get_result(uint256 competitor_index) public view returns(uint256){
        VoteStorage voteStorage = VoteStorage(address(voteStorages[voteStorageIndex]));
        return voteStorage.get_result(competitor_index);
    }

}
