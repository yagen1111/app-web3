// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TeslaToken is ERC20, Ownable {
    uint256 public priceUSD;

    constructor() ERC20("Tesla Token", "TSLA") Ownable(msg.sender) {
        _mint(msg.sender, 1000 * 10 ** decimals());
    }

    function updatePrice(uint256 newPriceUSD) public onlyOwner {
        priceUSD = newPriceUSD;
    }

    function getPriceUSD() public view returns (uint256) {
        return priceUSD;
    }
}

