from eth_utils import from_wei
from web3 import Web3

from .сonfig import EVMConnection

class EVMTools:
    def __init__(self, network_name):
        self.connection = EVMConnection(network_name)



    def get_balance(self, address):
        web3 = self.connection.get_web3_instance()

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


