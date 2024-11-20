import requests
from django.core.cache import cache
from .wallet_analysis import EVMTools


def network_info(request):
    """
    Контекст-процессор для предоставления данных о криптовалюте и сети.
    """
    # Инициализация EVMTools для данных сети
    evm_tools = EVMTools("ethereum_mainnet")
    try:
        gas_price = evm_tools.get_gas_price()
        latest_block = evm_tools.get_latest_block()
    except Exception as e:
        print("Error fetching network info:", e)
        gas_price = "N/A"
        latest_block = "N/A"

    # Ключи для кеша
    market_cap_key = 'total_market_cap'
    fear_greed_key = 'fear_greed_index'
    bitcoin_dominance_key = 'bitcoin_dominance'

    # Проверяем данные в кеше
    market_cap = cache.get(market_cap_key)
    fear_greed = cache.get(fear_greed_key)
    bitcoin_dominance = cache.get(bitcoin_dominance_key)

    if not (market_cap and fear_greed and bitcoin_dominance):
        try:
            # CoinGecko API для общей рыночной капитализации и Bitcoin Dominance
            coingecko_url = "https://api.coingecko.com/api/v3/global"
            coingecko_response = requests.get(coingecko_url).json()

            market_cap = coingecko_response["data"]["total_market_cap"]["usd"]
            bitcoin_dominance = coingecko_response["data"]["market_cap_percentage"]["btc"]

            # Alternative.me API для Fear & Greed Index
            fear_greed_url = "https://api.alternative.me/fng/"
            fear_greed_response = requests.get(fear_greed_url).json()

            fear_greed = fear_greed_response["data"][0]["value"]

            # Сохраняем данные в кеше на 1 час
            cache.set(market_cap_key, f"${market_cap:,.2f}", timeout=3600)
            cache.set(fear_greed_key, f"{fear_greed} (out of 100)", timeout=3600)
            cache.set(bitcoin_dominance_key, f"{bitcoin_dominance:.2f}%", timeout=3600)
        except Exception as e:
            print("Error fetching crypto data:", e)
            market_cap = "N/A"
            fear_greed = "N/A"
            bitcoin_dominance = "N/A"

    return {
        'gas_price': gas_price,
        'latest_block': latest_block,
        'total_market_cap': market_cap,
        'fear_greed_index': fear_greed,
        'bitcoin_dominance': bitcoin_dominance,
    }
