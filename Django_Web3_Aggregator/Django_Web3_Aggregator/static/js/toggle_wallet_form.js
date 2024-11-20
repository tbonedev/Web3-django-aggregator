document.addEventListener('DOMContentLoaded', () => {
    const connectWalletBtn = document.getElementById('connectWalletBtn');
    const walletDropdown = document.getElementById('walletDropdown');

    connectWalletBtn?.addEventListener('click', () => {
        walletDropdown.classList.toggle('show');
    });

    document.addEventListener('click', (event) => {
        if (!walletDropdown.contains(event.target) && event.target !== connectWalletBtn) {
            walletDropdown.classList.remove('show');
        }
    });
});
