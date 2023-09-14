// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@zeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "../interfaces/VRFCoordinatorV2Interface.sol";
import "../interfaces/LinkTokenInterface.sol";
import "./test/VRFCoordinatorV2Mock.sol";


contract Lottery is VRFConsumerBaseV2, Ownable {
    AggregatorV3Interface priceFeed;
    
    uint256 constant public entranceFeeInUsd = 50*(10**18);
    address payable[] users;
    address payable winner;
    uint256 randomNumber;
    
    bytes32 keyHash;
    uint64 subscriptionId;
    uint16 requestConfirmations;
    uint32 callbackGasLimit;
    uint32 numWords;

    //for active network:
    //VRFCoordinatorV2Interface vrfCoordinatorV2;
    //for testnet:
    VRFCoordinatorV2Mock vrfCoordinatorV2;

    LinkTokenInterface linkToken;

    uint256 _requestId;

    //address owner;

    enum LotteryState {
        OPEN,
        CLOSED,
        CALCULATING
        }

    LotteryState lotteryState = LotteryState.CLOSED;

    constructor(
        address _priceFeed,
        address _vrfCoordinatorV2,
        bytes32 _keyHash,
        //uint64 _subscriptionId,
        uint16 _requestConfirmations,
        uint32 _callbackGasLimit,
        uint32 _numWords,
        address _link
    ) VRFConsumerBaseV2(_vrfCoordinatorV2) {
        priceFeed = AggregatorV3Interface(_priceFeed);

        keyHash = _keyHash;
        //subscriptionId = _subscriptionId;
        //we will create new subscription!
        //subscriptionId = 0;
        requestConfirmations = _requestConfirmations;
        callbackGasLimit = _callbackGasLimit;
        numWords = _numWords;

        //for active network:
        //vrfCoordinatorV2 = VRFCoordinatorV2Interface(_vrfCoordinatorV2);
        //for testnet:
        vrfCoordinatorV2 = VRFCoordinatorV2Mock(_vrfCoordinatorV2);

        createNewSubscription();

        linkToken = LinkTokenInterface(_link);
    }
    
    function fulfillRandomWords(
        uint256 _requestId,
        uint256[] memory _randomWords
    ) internal override {
        require(lotteryState == LotteryState.CALCULATING, "Lottery isnt calculating");
        randomNumber = _randomWords[0];
        require(randomNumber > 0, "random-not-found");
        uint256 winner_i = randomNumber % users.length;
        winner = users[winner_i];
        winner.transfer(address(this).balance);
        lotteryState = LotteryState.CLOSED;
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
        _requestId = requestId;
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
        vrfCoordinatorV2.cancelSubscription(subscriptionId, owner());
        subscriptionId = 0;
    }
    function getSubscriptionId() public view returns(uint64){
        return subscriptionId;
    }
    function topUpSubscription(uint256 amount) external onlyOwner {
        linkToken.transferAndCall(
            address(vrfCoordinatorV2),
            amount,
            abi.encode(subscriptionId)
        );
    }

    modifier minimalEntryFee {
        require(msg.value >= getFeeInEthWei(), "send higher entry fee!");
        _;
    }

    function openLottery() public onlyOwner() {
        require(lotteryState == LotteryState.CLOSED, "Lottery cant be open");
        lotteryState = LotteryState.OPEN;
        users = new address payable[](0);
        randomNumber = 0;
        winner = payable(address(0));
    }

    function enterLottery() public payable minimalEntryFee() {
        require(lotteryState == LotteryState.OPEN, "Lottery isnt open");
        users.push(payable(msg.sender));
    }

    function endLottery() public onlyOwner() {
        require(lotteryState == LotteryState.OPEN, "Lottery cant be ended");
        lotteryState = LotteryState.CALCULATING;
        generateRandomNumber();
    }

    function getRequestId() public view returns(uint256) {
        return _requestId;
    }

    function getUsers() public view returns(address payable[] memory) {
        return users;
    }
}