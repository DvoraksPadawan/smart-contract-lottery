// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@zeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";


contract Lottery is VRFConsumerBaseV2, Ownable {
    AggregatorV3Interface priceFeed;
    
    uint256 constant entranceFeeInUsd = 50*(10**18);
    address payable[] users;
    uint256 randomNumber;
    
    bytes32 keyHash;
    uint64 subscriptionId;
    uint16 requestConfirmations;
    uint32 callbackGasLimit;
    uint32 numWords;

    VRFCoordinatorV2Interface vrfCoordinatorV2;

    //address owner;

    enum LotteryState {
        OPEN,
        CLOSED,
        CALCULATING
        }

    constructor(
        address _priceFeed,
        address _vrfCoordinatorV2,
        bytes32 _keyHash,
        //uint64 _subscriptionId,
        uint16 _requestConfirmations,
        uint32 _callbackGasLimit,
        uint32 _numWords
    ) VRFConsumerBaseV2(_vrfCoordinatorV2) {
        priceFeed = AggregatorV3Interface(_priceFeed);

        keyHash = _keyHash;
        //subscriptionId = _subscriptionId;
        //we will create new subscription!
        //subscriptionId = 0;
        requestConfirmations = _requestConfirmations;
        callbackGasLimit = _callbackGasLimit;
        numWords = _numWords;

        vrfCoordinatorV2 = VRFCoordinatorV2Interface(_vrfCoordinatorV2);

        createNewSubscription();

        //owner = msg.sender;
    }
    
     function fulfillRandomWords(
        uint256 _requestId,
        uint256[] memory _randomWords
    ) internal override {
        randomNumber = _randomWords[0];
    }

    function setSubscription(uint64 _subscriptionId) public onlyOwner() {
        subscriptionId = _subscriptionId;
    }

    function generateRandomNumber()
        public returns (uint256 requestId) {
        requestId = vrfCoordinatorV2.requestRandomWords(
            keyHash,
            subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );
        return requestId;
    }

    function getPriceOfEth() public view returns(uint256) {
        (,int256 intPrice,,,) = priceFeed.latestRoundData();
        uint256 price = uint256(intPrice) * (10**10);
        return price;
    }

    function getFeeInEthWei() public view returns(uint256) {
        uint256 fee = (entranceFeeInUsd * (10**18)) / getPriceOfEth();
        return fee;
    }

    function getLastRandomNumber() public view returns(uint256) {
        return randomNumber;
    }

    function createNewSubscription() private onlyOwner {
        subscriptionId = vrfCoordinatorV2.createSubscription();
        // Add this contract as a consumer of its own subscription.
        vrfCoordinatorV2.addConsumer(subscriptionId, address(this));
    }
    function cancelSubscription() external onlyOwner {
        // Cancel the subscription and send the remaining LINK to a wallet address.
        COORDINATOR.cancelSubscription(subscriptionId, owner);
        subscriptionId = 0;
    }
}