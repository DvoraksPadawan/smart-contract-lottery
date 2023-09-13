from brownie import accounts, network, config, VRFCoordinatorV2Mock, MockV3Aggregator, MockLinkToken, interface
ACTIVE_NETWORKS = ["Sepolia"]

def get_network():
    return network.show_active()

def get_account(i = 0):
    if network.show_active() == "development":
        return accounts[i]
    if network.show_active() in ACTIVE_NETWORKS:
        string = "account_" + str(i)
        return accounts.add(config["wallets"][string])

# DECIMALS = 8
# INITIAL_VALUE = 200000000000
def get_price_feed_address(decimals = 8, initial_value = 1500*10**8, i = 0):
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["price_feed"]
    else:
        account = accounts[i]
        price_feed_mock = MockV3Aggregator.deploy(decimals, initial_value, {"from": account}).address
        return price_feed_mock

def get_vrf_coordinator2_contract(baseFee = 10**18, gasPriceLink = 10**9, i = 0):
    if network.show_active() in ACTIVE_NETWORKS:
        vrf_coordinator_address = config["networks"][network.show_active()]["vrf_coordinator2"]
        return interface.VRFCoordinatorV2Interface(vrf_coordinator_address)
    else:
        account = accounts[i]
        vrf_mock = VRFCoordinatorV2Mock.deploy(baseFee, gasPriceLink, {"from": account})
        return vrf_mock
        
    
def get_key_hash():
    return config["networks"][network.show_active()]["key_hash"]
    
def get_subscriptionId():
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["subscriptionId"]
    
def get_requestConfirmations():
    return config["networks"][network.show_active()]["requestConfirmations"]
    
def get_callbackGasLimit():
     return config["networks"][network.show_active()]["callbackGasLimit"]
    
def get_numWords():
     return config["networks"][network.show_active()]["numWords"]
    
def get_link_contract(i = 0):
    if network.show_active() in ACTIVE_NETWORKS:
        link_address = config["networks"][network.show_active()]["link"]
        return interface.LinkTokenInterface(link_address)
    else:
        account = accounts[i]
        link_mock = MockLinkToken.deploy({"from": account})
        return link_mock
    
def get_publish_source():
     return config["networks"][network.show_active()]["verify"]

    
