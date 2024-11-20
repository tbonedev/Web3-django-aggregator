import requests

# Инициализация API-ключа Moralis
MORALIS_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImVjM2IxMDMwLTUxNjktNDUwYi1iYmUwLTAwZDNkMjJmNmZmOSIsIm9yZ0lkIjoiNDE2NDc0IiwidXNlcklkIjoiNDI4MDc5IiwidHlwZUlkIjoiNTQwYzQyZWEtYWMyMS00YmZlLTk5YzMtYjVlMjU4MDdhMjM4IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MzE4Mjk5NTcsImV4cCI6NDg4NzU4OTk1N30.G0K-qMoGK52QJy5Sske8i1kdZVasIdo3S7gEPXWc-8Q"

def get_defi_summary(wallet_address, chain="eth"):
    """
    Получает DeFi summary для указанного кошелька.
    """
    url = f"https://deep-index.moralis.io/api/v2.2/wallets/{wallet_address}/defi/summary"
    headers = {"X-API-Key": MORALIS_API_KEY}
    params = {"chain": chain}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()  # Возвращаем ответ JSON
        else:
            print(f"Ошибка: {response.status_code} - {response.text}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return {}

# Замените адрес кошелька на реальный
wallet_address = "0x9d17bb55b57b31329cf01aa7017948e398b277bc"

# Получаем и выводим DeFi summary
defi_summary = get_defi_summary(wallet_address)
print("DeFi Summary:")
print(defi_summary)
