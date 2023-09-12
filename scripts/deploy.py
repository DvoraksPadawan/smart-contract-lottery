from brownie import Lottery, interface, VRFCoordinatorV2Mock
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

        self._link = helpful_scripts.get_link_address()

        self.publish_source = helpful_scripts.get_publish_source()
        
        self.lottery = Lottery.deploy(self._price_feed,
                                      self._vrf_coordinator2,
                                      self.key_hash,
                                      #self.subscriptionId,
                                      self.requestConfirmations,
                                      self.callbackGasLimit,
                                      self.numWords,
                                      self._link, 
                                      {"from": account},
                                      publish_source=self.publish_source)
        
        if (helpful_scripts.get_network() == "development"):
            #self.vrf_coordinator2 = VRFCoordinatorV2Mock(self._vrf_coordinator2)
            self.vrf_coordinator2 = VRFCoordinatorV2Mock[-1]
        else:
            self.vrf_coordinator2 = interface.VRFCoordinatorV2Interface(self._vrf_coordinator2)
        #self._link = helpful_scripts.get_link_address()
        self.link = interface.LinkTokenInterface(self._link)
        print("address:", self.lottery.address)
        self.subscriptionId = self.lottery.getSubscriptionId()
        print(self.subscriptionId)
        print("subscripton:", self.vrf_coordinator2.getSubscription(self.subscriptionId))

    def request_random_number(self, account = None):
        account = account if account else helpful_scripts.get_account()
        tx = self.lottery.generateRandomNumber( {"from" : account})
        if (helpful_scripts.get_network() == "development"):
            requestId = self.lottery.getRequestId()
            tx = self.vrf_coordinator2.fulfillRandomWords(requestId, self.lottery.address, {"from": account})
            return
        tx.wait(5)
        return self.lottery.getLastRandomNumber()
    
    def create_subscription2(self, account = None):
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

    def cancel_subscription2(self, account = None):
        account = account if account else helpful_scripts.get_account()
        print("subscripton:", self.vrf_coordinator2.getSubscription(self.subscriptionId))
        tx = self.vrf_coordinator2.cancelSubscription(self.subscriptionId, account, {"from" : account})
        #amount = self.link.balanceOf(account)
        #tx = self.link.transfer(account, amount, {"from" : account})
        print("subscripton:", self.vrf_coordinator2.getSubscription(self.subscriptionId))

    def cancel_subscription(self, account = None):
        account = account if account else helpful_scripts.get_account()
        print("subscripton:", self.vrf_coordinator2.getSubscription(self.subscriptionId))
        tx = self.lottery.cancelSubscription({"from" : account})
        if (helpful_scripts.get_network() == "development"):
            return
        tx.wait(5)
        

    def fund_with_link(self, amount, account = None):
        account = account if account else helpful_scripts.get_account()
        if (helpful_scripts.get_network() == "development"):
            self.vrf_coordinator2.fundSubscription(self.subscriptionId, amount)
            print("mock funded")
            print("subscripton:", self.vrf_coordinator2.getSubscription(self.subscriptionId))
            return
        tx = self.link.approve(self.lottery.address, amount, {"from" : account})
        tx.wait(5)
        print("approved")
        tx = self.link.transfer(self.lottery.address, amount, {"from" : account})
        tx.wait(5)
        print("contract funded")
        tx = self.lottery.topUpSubscription(amount, {"from" : account})
        tx.wait(5)
        print("subscripton:", self.vrf_coordinator2.getSubscription(self.subscriptionId))

    def fund_mock(self, amount, account):
        self.vrf_coordinator2.fundSubscription(self.subscriptionId, amount)






def main():
    lottery = Lottery_class()
    print("random number:", lottery.lottery.getLastRandomNumber())
    print("price:", lottery.lottery.getPriceOfEth())
    print("fee:", lottery.lottery.getFeeInEthWei())
    input()
    lottery.fund_with_link(20*(10**18))
    input()
    lottery.request_random_number()
    print("random number:", lottery.lottery.getLastRandomNumber())
    input()
    lottery.cancel_subscription()
    #print("subscripton:", lottery.vrf_coordinator2.getSubscription(lottery.subscriptionId))
    #print("random number:", lottery.request_random_number())

def print_decimal_fee(fee = 25):
    print(fee*10**16)