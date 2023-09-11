from brownie import Lottery, interface
import scripts.helpful_scripts as helpful_scripts


class Lottery_class:
    def __init__(self, account = None):
        account = account if account else helpful_scripts.get_account()
        self._price_feed = helpful_scripts.get_price_feed_address()

        self._vrf_coordinator2 = helpful_scripts.get_vrf_coordinator2_address()
        self.key_hash = helpful_scripts.get_key_hash()
        #self.subscriptionId = helpful_scripts.get_subscriptionId()
        self.requestConfirmations = helpful_scripts.get_requestConfirmations()
        self.callbackGasLimit = helpful_scripts.get_callbackGasLimit()
        self.numWords = helpful_scripts.get_numWords()
        
        self.lottery = Lottery.deploy(self._price_feed,
                                      self._vrf_coordinator2,
                                      self.key_hash,
                                      #self.subscriptionId,
                                      self.requestConfirmations,
                                      self.callbackGasLimit,
                                      self.numWords,
                                      {"from": account},
                                      publish_source=True)
        
        
        self.vrf_coordinator2 = interface.VRFCoordinatorV2Interface(self._vrf_coordinator2)
        #self._link = helpful_scripts.get_link_address()
        #self.link = interface.LinkTokenInterface(self._link)
        print("address:", self.lottery.address)

    def request_random_number(self, account = None):
        account = account if account else helpful_scripts.get_account()
        tx = self.lottery.generateRandomNumber( {"from" : account})
        tx.wait(10)
        print("random number:", self.lottery.getLastRandomNumber())
        return self.lottery.getLastRandomNumber()
    
    def create_subscription(self, account = None):
        account = account if account else helpful_scripts.get_account()
        tx = self.vrf_coordinator2.createSubscription({"from" : account})
        print(tx.events)
        #print("1" + tx.events['(unknown)'])
        print(tx.events['(unknown)'][0])
        print("3" + tx['(unknown)'][0]['topic2'])
        #hex = tx.events["topic2"]
        #self.subscriptionId = int(hex, 16)
        #print(hex)
        tx.wait(10)
        print(tx.events)
        print("subscripton:", self.vrf_coordinator2.getSubscription(self.subscriptionId))
        tx = self.vrf_coordinator2.addConsumer(self.subscriptionId, self.lottery.address, {"from" : account})
        tx.wait(10)
        print("subscripton:", self.vrf_coordinator2.getSubscription(self.subscriptionId))

    def cancel_subscription(self, account = None):
        account = account if account else helpful_scripts.get_account()
        print("subscripton:", self.vrf_coordinator2.getSubscription(self.subscriptionId))
        tx = self.vrf_coordinator2.cancelSubscription(self.subscriptionId, account, {"from" : account})
        #amount = self.link.balanceOf(account)
        #tx = self.link.transfer(account, amount, {"from" : account})
        print("subscripton:", self.vrf_coordinator2.getSubscription(self.subscriptionId))





def main():
    lottery = Lottery_class()
    print("random number:", lottery.lottery.getLastRandomNumber())
    print("price:", lottery.lottery.getPriceOfEth())
    print("fee:", lottery.lottery.getFeeInEthWei())
    input()
    lottery.create_subscription()
    input()
    lottery.cancel_subscription()
    #lottery.fund_with_link()
    #lottery.lottery.getLastRandomNumber()
    print("random number:", lottery.request_random_number())

def print_decimal_fee(fee = 25):
    print(fee*10**16)