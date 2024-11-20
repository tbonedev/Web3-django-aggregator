function loadMoreNFTs(network) {
    const button = document.querySelector(`.load-more-btn[data-network="${network}"]`);
    if (!button) {
        console.error(`Button for network "${network}" not found.`);
        return;
    }

    const page = parseInt(button.getAttribute("data-page"), 10);

    fetch(`/wallets/balance/?network=${network}&page=${page}`, {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.nfts && data.nfts.length > 0) {
                const nftGrid = document.getElementById(`nft-grid-${network}`);
                if (!nftGrid) {
                    console.error(`Grid for network "${network}" not found.`);
                    return;
                }

                data.nfts.forEach((nft) => {
                    const nftCard = document.createElement("div");
                    nftCard.className = "nft-card";
                    nftCard.innerHTML = `
                        <img src="${nft.image_url}" alt="NFT Image" class="nft-image">
                        <h4 class="nft-name" title="${nft.name}">${nft.name}</h4>
                        <a href="${nft.permalink}" target="_blank" class="nft-link">View on OpenSea</a>
                    `;
                    nftGrid.appendChild(nftCard);
                });

                button.setAttribute("data-page", page + 1);

                if (!data.has_more) {
                    button.style.display = "none";
                }
            } else {
                console.warn("No more NFTs to load.");
                button.style.display = "none";
            }
        })
        .catch((error) => {
            console.error("Error loading more NFTs:", error);
        });
}
