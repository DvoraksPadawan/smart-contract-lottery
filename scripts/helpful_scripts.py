from brownie import accounts, network, config, VRFCoordinatorV2Mock, MockV3Aggregator, MockLinkToken
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

def get_vrf_coordinator2_address(baseFee = 10**18, gasPriceLink = 10**9, i = 0):
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["vrf_coordinator2"]
    else:
        account = accounts[i]
        vrf_mock = VRFCoordinatorV2Mock.deploy(baseFee, gasPriceLink, {"from": account}).address
        return vrf_mock
        
    
def get_key_hash():
    #if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["key_hash"]
    
def get_subscriptionId():
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["subscriptionId"]
    
def get_requestConfirmations():
    #if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["requestConfirmations"]
    
def get_callbackGasLimit():
    #if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["callbackGasLimit"]
    
def get_numWords():
    #if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["numWords"]
    
def get_link_address(i = 0):
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["link"]
    else:
        account = accounts[i]
        link_mock = MockLinkToken.deploy({"from": account}).address
        return link_mock
    
def get_publish_source():
     return config["networks"][network.show_active()]["verify"]

    
