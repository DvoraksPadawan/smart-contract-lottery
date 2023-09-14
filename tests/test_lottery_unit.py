from scripts.deploy import Lottery_class
from scripts import helpful_scripts
from brownie import exceptions
import pytest

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

def test_can_open_lottery():
    lottery = Lottery_class()
    account_0 = helpful_scripts.get_account(0)
    account_1 = helpful_scripts.get_account(1)
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.lottery.endLottery({"from": account_0})
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.lottery.openLottery({"from": account_1})
    lottery.lottery.openLottery({"from": account_0})

def test_can_enter_lottery():
    lottery = Lottery_class()
    account_0 = helpful_scripts.get_account(0)
    account_1 = helpful_scripts.get_account(1)
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.lottery.enterLottery({"from": account_0})
    lottery.lottery.openLottery({"from": account_0})
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.lottery.enterLottery({"from": account_0})
    entry_fee = lottery.lottery.getFeeInEthWei()
    eth_price = lottery.lottery.getPriceOfEth()
    fee_in_usd = lottery.lottery.entranceFeeInUsd()
    result = ((fee_in_usd*10**18)/eth_price)
    assert entry_fee >= result - 2
    assert entry_fee <= result + 2
    users = lottery.lottery.getUsers()
    assert len(users) == 0
    lottery.lottery.enterLottery({"from": account_0, "value": entry_fee})
    users = lottery.lottery.getUsers()
    assert len(users) == 1
    lottery.lottery.enterLottery({"from": account_1, "value": entry_fee})
    users = lottery.lottery.getUsers()
    assert len(users) == 2
    lottery.lottery.enterLottery({"from": account_0, "value": entry_fee})
    users = lottery.lottery.getUsers()
    assert len(users) == 3

def test_cant_get_random_number():
    lottery = Lottery_class()
    account_0 = helpful_scripts.get_account(0)
    lottery.lottery.openLottery({"from": account_0})
    amount = 20*(10**18)
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.request_random_number()
    assert lottery.lottery.getLastRandomNumber() == 0

def test_can_make_winner():
    lottery = Lottery_class()
    account_0 = helpful_scripts.get_account(0)
    account_1 = helpful_scripts.get_account(1)
    lottery.lottery.openLottery({"from": account_0})
    entry_fee = lottery.lottery.getFeeInEthWei()
    lottery.lottery.enterLottery({"from": account_0, "value": entry_fee})
    lottery.lottery.enterLottery({"from": account_1, "value": entry_fee})
    lottery.lottery.enterLottery({"from": account_0, "value": entry_fee})
    assert lottery.lottery.balance() == 3*lottery.lottery.getFeeInEthWei()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.end_lottery()
    amount = 20*(10**18)
    lottery.fund_with_link(amount)
    assert lottery.lottery.getLastRandomNumber() == 0
    account = account_0
    starting_balance = account.balance()
    reward = lottery.lottery.balance()
    assert len(lottery.lottery.getUsers()) > 0
    lottery.end_lottery()
    assert lottery.lottery.getLastRandomNumber() > 0
    assert reward > 0
    assert lottery.lottery.balance() == 0
    assert account.balance() == starting_balance + reward
    lottery.lottery.openLottery({"from": account_0})
    assert len(lottery.lottery.getUsers()) == 0
