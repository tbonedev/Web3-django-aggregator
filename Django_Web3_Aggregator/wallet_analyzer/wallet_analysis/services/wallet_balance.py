# wallet_analyzer/services/wallet_balance.py

from eth_utils import from_wei
from web3 import Web3

from ...wallet_analysis import EVMConnection


class WalletBalance:
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
        self.supported_chains = {
            "ethereum": EVMConnection("ethereum_mainnet"),
            "polygon": EVMConnection("polygon_mainnet"),
            "avalanche": EVMConnection("avalanche_mainnet"),
            "base": EVMConnection("base_mainnet"),
            "zora": EVMConnection("zora_mainnet"),
        }

    def get_balances(self):
        """
        Получает балансы кошелька для всех поддерживаемых сетей.
        """
        balances = {}
        for chain, connection in self.supported_chains.items():
            web3_instance = connection.get_web3_instance()
            checksum_address = Web3.to_checksum_address(self.wallet_address)
            balance_wei = web3_instance.eth.get_balance(checksum_address)
            balances[chain.capitalize()] = round(from_wei(balance_wei, 'ether'), 4)
        return balances
