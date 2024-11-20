// metamask_connection_check.js

// Функция для проверки, подключен ли MetaMask
async function checkMetaMaskConnected() {
    if (typeof window.ethereum !== 'undefined') {
        const accounts = await window.ethereum.request({ method: 'eth_accounts' });
        return accounts.length > 0;
    }
    return false;
}

// Выполняем проверку подключения MetaMask при загрузке страницы
document.addEventListener("DOMContentLoaded", async function() {
    const isConnected = await checkMetaMaskConnected();
    const currentPath = window.location.pathname;

    // Укажите пути, где требуется проверка MetaMask
    const restrictedPaths = ['/wallets/balance/', '/wallets/more_info/'];

    if (!isConnected && restrictedPaths.includes(currentPath)) {
        alert("MetaMask не подключен. Пожалуйста, подключите MetaMask для доступа к функционалу сайта.");

        // Отправляем запрос на сервер для очистки сессии
        await fetch('/wallets/disconnect/', {
            method: 'POST',
            headers: { 'X-CSRFToken': window.csrfToken } // Используем глобальный CSRF-токен
        });

        // Перенаправляем на главную страницу после очистки сессии
        window.location.href = '/';
    }
});