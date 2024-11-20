import requests

class WalletNFTs:
    def __init__(self, wallet_address, api_key, supported_chains=None):
        self.wallet_address = wallet_address
        self.api_key = api_key
        self.supported_chains = supported_chains or ["ethereum", "polygon", "avalanche", "base", "zora"]

    def get_nfts(self, chain="ethereum", offset=0, limit=5):
        print(f"Fetching NFTs for chain: {chain}, Offset: {offset}, Limit: {limit}")

        opensea_url = (
            f"https://api.opensea.io/api/v2/chain/{chain}/account/{self.wallet_address}/nfts"
            f"?offset={offset}&limit={limit}"
        )
        headers = {
            "Accept": "application/json",
            "X-API-KEY": self.api_key,
        }

        try:
            response = requests.get(opensea_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                nfts = []
                for nft in data.get("nfts", []):
                    if not isinstance(nft, dict):
                        continue

                    contract_address = nft.get("contract")
                    token_id = nft.get("identifier")
                    if not contract_address or not token_id:
                        continue

                    image_url = nft.get("display_image_url") or nft.get("image_url") or "https://via.placeholder.com/150"

                    permalink = f"https://opensea.io/assets/{chain}/{contract_address}/{token_id}"

                    nfts.append({
                        "name": nft.get("name", "Unnamed NFT"),
                        "image_url": image_url,
                        "permalink": permalink,
                    })
                return nfts
            else:
                print(f"Error fetching NFTs: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return []

    def get_all_nfts_for_chain(self, chain, limit=50):
        """
        Получает все NFT для одной сети.
        """
        offset = 0
        all_nfts = []

        while True:
            nfts = self.get_nfts(chain=chain, offset=offset, limit=limit)
            if not nfts:
                break
            all_nfts.extend(nfts)
            offset += limit

        return all_nfts

    def get_all_nfts(self):
        """
        Получает все NFT для всех поддерживаемых сетей.
        """
        all_nfts = {}
        for chain in self.supported_chains:
            all_nfts[chain.capitalize()] = self.get_all_nfts_for_chain(chain)
        return all_nfts
