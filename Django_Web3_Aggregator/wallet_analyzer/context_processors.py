# wallet_analyzer/context_processors.py
from .wallet_analysis.utils import EVMTools


def network_info(request):
    evm_tools = EVMTools("ethereum_mainnet")
    gas_price = evm_tools.get_gas_price()
    latest_block = evm_tools.get_latest_block()

    return {
        'gas_price': gas_price,
        'latest_block': latest_block,
    }
