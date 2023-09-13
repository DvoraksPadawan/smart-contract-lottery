from scripts.deploy import Lottery_class
from scripts import helpful_scripts

def test_can_get_price():
    lottery = Lottery_class()
    eth_price = lottery.lottery.getPriceOfEth()
    assert eth_price == 1500*10**18

def test_can_send_link():
    lottery = Lottery_class()
    account_0 = helpful_scripts.get_account(0)
    account_1 = helpful_scripts.get_account(1)
    amount = 10**18
    starting_balance = lottery.link.balanceOf(account_0)
    lottery.link.transfer(account_1, amount, {"from": account_0})
    assert lottery.link.balanceOf(account_0) == starting_balance - amount
    assert lottery.link.balanceOf(account_1) == amount