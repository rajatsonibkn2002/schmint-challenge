// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts@4.7.3/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts@4.7.3/access/Ownable.sol";

contract Role is ERC1155, Ownable {
    constructor() ERC1155("") {}

    uint constant Schmint = 1;
    uint constant OG = 2;
    uint constant Simplr = 3;

    modifier onlyOne(address _account, uint _id){
        require(balanceOf(_account, _id)==0, "User already has a token");
        _;
    }

    event mintRole(string _discord, uint _id);

    function mint(address _account, uint256 _id, string memory _discord)
        public
        onlyOne(_account, _id)
        onlyOwner
    {
        require(_id==1 ||_id==2 || _id==3, "Invalid Token ID");
        _mint(_account, _id, 1, "");
        emit mintRole(_discord, _id);
    }

}
