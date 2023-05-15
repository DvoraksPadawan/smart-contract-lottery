
import scripts.helpful_scripts as helpful_scripts
from brownie import Lottery, interface

class Lottery_class:
    def __init__(self, account = None):
        account = account if account else helpful_scripts.get_account()
        self._price_feed = helpful_scripts.get_price_feed_address()

        self._vrf_coordinator2 = helpful_scripts.get_vrf_coordinator2_address()
        self.key_hash = helpful_scripts.get_key_hash()
        self.subscriptionId = helpful_scripts.get_subscriptionId()
        self.requestConfirmations = helpful_scripts.get_requestConfirmations()
        self.callbackGasLimit = helpful_scripts.get_callbackGasLimit()
        self.numWords = helpful_scripts.get_numWords()
        
        self.lottery = Lottery.deploy(self._price_feed,
                                      self._vrf_coordinator2,
                                      self.key_hash,
                                      self.subscriptionId,
                                      self.requestConfirmations,
                                      self.callbackGasLimit,
                                      self.numWords,
                                      {"from": account},
                                      publish_source=True)
        
        print("address:", self.lottery.address)
        print("subscripton:", interface.VRFCoordinatorV2Interface(self._vrf_coordinator2).getSubscription(self.subscriptionId))
        tx = interface.VRFCoordinatorV2Interface(self._vrf_coordinator2).addConsumer(self.subscriptionId, self.lottery.address, {"from" : account})
        print("subscripton:", interface.VRFCoordinatorV2Interface(self._vrf_coordinator2).getSubscription(self.subscriptionId))
        tx.wait(10)
        print("subscripton:", interface.VRFCoordinatorV2Interface(self._vrf_coordinator2).getSubscription(self.subscriptionId))

    def fund_with_link(self, account = None, amount = 0):
        account = account if account else helpful_scripts.get_account()
        #if (amount == 0): amount = self.link_fee
        amount = amount if amount > 0 else 2 * self.link_fee
        interface.LinkTokenInterface(self._link).transfer(self.lottery.address, amount, {"from" : account})

    def request_random_number(self, account = None):
        account = account if account else helpful_scripts.get_account()
        tx = self.lottery.generateRandomNumber( {"from" : account})
        tx.wait(1)
        print("random number:", self.lottery.getLastRandomNumber())
        return self.lottery.getLastRandomNumber()



def main():
    lottery = Lottery_class()
    print("random number:", lottery.lottery.getLastRandomNumber())
    print("price:", lottery.lottery.getPriceOfEth())
    print("fee:", lottery.lottery.getFeeInEthWei())
    #lottery.fund_with_link()
    lottery.lottery.getLastRandomNumber()
    print("random number:", lottery.request_random_number())

def print_decimal_fee(fee = 25):
    print(fee*10**16)