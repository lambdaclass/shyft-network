// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ConversionRateProvider {
    uint256 public conversionRate;

    constructor(uint256 _conversionRate) {
        conversionRate = _conversionRate;
    }

    // This function needs a modifier, since it can be called from a whitelisted address.
    function setConversionRate(
        uint256 newConversionRate
    ) external {
        conversionRate = newConversionRate;
    }

    function getConversionRate() external view returns (uint256) {
        return conversionRate;
    }
}
