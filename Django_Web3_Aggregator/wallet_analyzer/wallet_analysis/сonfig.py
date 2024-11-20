# config.py
from web3 import Web3

class EVMConnection:
    networks = {
        "ethereum_mainnet": "https://eth.llamarpc.com",
        "polygon_mainnet": "https://polygon.llamarpc.com",
        "avalanche_mainnet": "https://avalanche-c-chain-rpc.publicnode.com",
        "bsc_mainnet": "https://binance.llamarpc.com",
        "base_mainnet": "https://base.llamarpc.com",
        "zora_mainnet": "https://zora.drpc.org",
    }

    def __init__(self, network_name):
        self.network_name = network_name
        self.web3 = Web3(Web3.HTTPProvider(self.networks[network_name]))


    def is_connected(self):
        return self.web3.is_connected()

    def get_web3_instance(self):
        return self.web3

# Автоматическое создание экземпляра при импорте файла
eth_connection = EVMConnection("ethereum_mainnet")
polygon_connection = EVMConnection("polygon_mainnet")
avalanche_connection = EVMConnection("avalanche_mainnet")
bsc_connection = EVMConnection("bsc_mainnet")
base_connection = EVMConnection("base_mainnet")
zora_connection = EVMConnection("zora_mainnet")

