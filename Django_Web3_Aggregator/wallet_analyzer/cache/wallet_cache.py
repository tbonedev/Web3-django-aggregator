from django.core.cache import cache

def get_cached_wallet_balance(wallet_address):
    balance_cache_key = f"wallet_balance_{wallet_address}"
    wallet_balance = cache.get(balance_cache_key)

    if not wallet_balance:
        from wallet_analyzer.wallet_analysis.services.wallet_balance import WalletBalance
        wallet_balance = WalletBalance(wallet_address).get_balances()
        cache.set(balance_cache_key, wallet_balance, timeout=3600)

    return wallet_balance


def get_cached_wallet_nfts(wallet_address):
    nfts_cache_key = f"wallet_nfts_{wallet_address}"
    wallet_nfts = cache.get(nfts_cache_key)

    if not wallet_nfts:
        from wallet_analyzer.wallet_analysis.services.nfts_on_wallet import WalletNFTs
        wallet_nfts = {
            network: WalletNFTs(wallet_address, api_key='e12879e3012940e186ae9277976fe41b').get_nfts(chain=network, offset=0, limit=5)
            for network in ["ethereum", "polygon", "avalanche", "base", "zora"]
        }
        cache.set(nfts_cache_key, wallet_nfts, timeout=3600)
    return wallet_nfts

def invalidate_cache(wallet_address):
    cache.delete(f"wallet_balance_{wallet_address}")
    cache.delete(f"wallet_nfts_{wallet_address}")
