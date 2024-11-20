from eth_utils import from_wei
from web3 import Web3


from ..wallet_analysis import EVMConnection


class EVMTools:
    def __init__(self, network_name):
        # Initialize the connection for the specified network
        self.connection = EVMConnection(network_name)

    @staticmethod
    def get_network_connections():
        # Create connections for each network and store in a dictionary
        return {
            "ethereum_mainnet": EVMConnection("ethereum_mainnet"),
            "polygon_mainnet": EVMConnection("polygon_mainnet"),
            "avalanche_mainnet": EVMConnection("avalanche_mainnet"),
            "bsc_mainnet": EVMConnection("bsc_mainnet"),
            "base_connection": EVMConnection("base_mainnet"),
            "zora_connection": EVMConnection("zora_mainnet")
        }

    def get_balance(self, address):
        # Get web3 instance from the connection
        web3 = self.connection.get_web3_instance()

        # Ensure the address is in checksum format
        checksum_address = Web3.to_checksum_address(address)
        balance_wei = web3.eth.get_balance(checksum_address)
        return from_wei(balance_wei, 'ether')

    def get_gas_price(self):
        web3 = self.connection.get_web3_instance()
        gas_price_wei = web3.eth.gas_price
        return from_wei(gas_price_wei, 'gwei')

    def get_latest_block(self):
        web3 = self.connection.get_web3_instance()
        latest_block = web3.eth.get_block('latest')
        return latest_block
