from brownie import Lottery

import scripts.helpful_scripts as helpful_scripts

def deploy(account = None):
    account = account if account else helpful_scripts.get_account()
    _price_feed = helpful_scripts.get_price_feed_address()
    _vrf_coordinator = helpful_scripts.get_vrf_coordinator_address()
    _link = helpful_scripts.get_link_address()
    key_hash = helpful_scripts.get_key_hash()
    lottery = Lottery.deploy(_vrf_coordinator, _link, _price_feed, key_hash, {"from": account})
    price = lottery.getPriceOfEth()
    fee = lottery.getFeeInEthWei()
    print(price)
    print(fee)

def fund_with_link(account = None, amount = 25*10**16):
    account = account if account else helpful_scripts.get_account()
    _link = helpful_scripts.get_link_address()
    lottery = Lottery[-1]
    _link.transfer(lottery.address, amount, {"from" : account})

    



def main():
    deploy()