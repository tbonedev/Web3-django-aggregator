document.addEventListener("DOMContentLoaded", () => {
    const connectWalletButton = document.getElementById("connectWalletButton");

    connectWalletButton.addEventListener("click", async function () {
        if (typeof window.ethereum !== 'undefined') {
            try {
                // Запрос адресов аккаунтов
                const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                const walletAddress = accounts[0];

                // Устанавливаем значение скрытого поля и отправляем форму
                document.getElementById("id_address").value = walletAddress;
                document.getElementById("walletForm").submit();
            } catch (error) {
                alert("Failed to connect to Metamask. " + error.message);
            }
        } else {
            alert("Metamask is not installed. Please install Metamask to use this feature.");
        }
    });
});
