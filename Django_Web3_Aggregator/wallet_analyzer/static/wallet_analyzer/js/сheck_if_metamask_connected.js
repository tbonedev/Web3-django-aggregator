// check_metamask_connected.js

async function checkMetaMaskConnected() {
    if (typeof window.ethereum !== 'undefined') {
        const accounts = await window.ethereum.request({ method: 'eth_accounts' });
        return accounts.length > 0;
    }
    return false;
}
