// handle_metamask_redirect.js

document.addEventListener("DOMContentLoaded", async function() {
    const isConnected = await checkMetaMaskConnected();
    const currentPath = window.location.pathname;

    // Добавляем нужные пути, где требуется проверка MetaMask
    const restrictedPaths = ['/wallets/balance/', '/wallets/more_info/'];

    if (!isConnected && restrictedPaths.includes(currentPath)) {
        alert("MetaMask не подключен. Пожалуйста, подключите MetaMask для доступа к функционалу сайта.");

        // Отправляем запрос на сервер для очистки сессии
        await fetch('/wallets/disconnect/', {
            method: 'POST',
            headers: { 'X-CSRFToken': window.csrfToken } // Подставьте корректный токен CSRF
        });

        // Перенаправляем на главную страницу после очистки сессии
        window.location.href = '/';
    }
});
