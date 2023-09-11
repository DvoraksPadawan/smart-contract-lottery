from brownie import accounts, network, config
ACTIVE_NETWORKS = ["Sepolia"]

def get_account(i = 0):
    if network.show_active() == "development":
        return accounts[i]
    if network.show_active() in ACTIVE_NETWORKS:
        string = "account_" + str(i)
        return accounts.add(config["wallets"][string])

def get_price_feed_address():
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["price_feed"]

def get_vrf_coordinator2_address():
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["vrf_coordinator2"]
    
def get_key_hash():
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["key_hash"]
    
def get_subscriptionId():
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["subscriptionId"]
    
def get_requestConfirmations():
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["requestConfirmations"]
    
def get_callbackGasLimit():
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["callbackGasLimit"]
    
def get_numWords():
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["numWords"]
    
def get_link_address():
    if network.show_active() in ACTIVE_NETWORKS:
        return config["networks"][network.show_active()]["link"]

    
