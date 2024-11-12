# config.py
from web3 import Web3

class EVMConnection:
    networks = {
        "ethereum_mainnet": "https://eth.llamarpc.com",
    }

    def __init__(self, network_name):
        self.network_name = network_name
        self.web3 = Web3(Web3.HTTPProvider(self.networks[network_name]))

        # Пример использования функции и вывода результата
        connection_status = self.is_connected()
        print("Подключение установлено" if connection_status else "Ошибка подключения")

    def is_connected(self):
        return self.web3.is_connected()

    def get_web3_instance(self):
        return self.web3

# Автоматическое создание экземпляра при импорте файла
eth_connection = EVMConnection("ethereum_mainnet")

