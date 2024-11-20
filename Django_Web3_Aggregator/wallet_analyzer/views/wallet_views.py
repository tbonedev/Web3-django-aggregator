from web3 import Web3


from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, FormView
from django.views import View

from ..forms import WalletForm
from ..models import Wallet

from ..wallet_analysis import WalletNFTs, EVMTools

from ..wallet_analysis.services import WalletBalance

from ..wallet_analysis.сonfig import eth_connection



class WalletConnectView(FormView):
    template_name = 'wallet_analyzer/components/wallet_connection.html'
    form_class = WalletForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        wallet_address = form.cleaned_data['address']

        # Проверяем, существует ли уже адрес в базе данных
        wallet, created = Wallet.objects.get_or_create(address=wallet_address)

        # Устанавливаем флаг в сессии для идентификации подключенного кошелька
        self.request.session['wallet_connected'] = True
        self.request.session['wallet_address'] = wallet.address

        return super().form_valid(form)


class WalletBalanceView(TemplateView):
    template_name = "wallet_analyzer/components/wallet_balance.html"

    def get(self, request, *args, **kwargs):
        # Если адрес кошелька отсутствует в сессии, перенаправляем на главную страницу
        if 'wallet_address' not in request.session:
            return HttpResponseRedirect(reverse_lazy('index'))

        # Проверяем, это AJAX-запрос для загрузки дополнительных NFT?
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return self.handle_ajax_request(request)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet_address = self.request.session.get('wallet_address')

        # Получаем только балансы и первые 5 NFT
        wallet_balance = WalletBalance(wallet_address)
        wallet_nfts = WalletNFTs(wallet_address, api_key="e12879e3012940e186ae9277976fe41b")

        context['address'] = wallet_address
        context['balances'] = wallet_balance.get_balances()

        # Отображаем первые 5 NFT для каждой сети
        nfts_by_network = {}
        for network in ["ethereum", "polygon", "avalanche", "base", "zora"]:
            nfts_by_network[network] = wallet_nfts.get_nfts(chain=network, offset=0, limit=5)

        context['nfts_by_network'] = nfts_by_network
        return context

    def handle_ajax_request(self, request):
        """
        Обработка AJAX-запросов для загрузки дополнительных NFT.
        """
        wallet_address = request.session.get('wallet_address')
        if not wallet_address:
            return JsonResponse({'error': 'Wallet address not found in session'}, status=400)

        # Извлекаем параметры из запроса
        network = request.GET.get('network')
        page = int(request.GET.get('page', 1))
        items_per_page = 5
        offset = (page - 1) * items_per_page

        # Создаем экземпляр WalletNFTs
        wallet_nfts = WalletNFTs(wallet_address, api_key="e12879e3012940e186ae9277976fe41b")

        # Получаем список NFT с учетом offset и limit
        paginated_nfts = wallet_nfts.get_nfts(chain=network, offset=offset, limit=items_per_page)

        # Логирование
        print(f"Network: {network}, Page: {page}, Offset: {offset}, NFTs returned: {len(paginated_nfts)}")

        # Возвращаем JSON-ответ
        return JsonResponse({
            'nfts': paginated_nfts,
            'has_more': len(paginated_nfts) == items_per_page,  # Есть ли еще NFT для загрузки
        })


class WalletDisconnectView(View):
    def post(self, request, *args, **kwargs):
        # Удаляем адрес кошелька и флаг из сессии, если они существуют
        if 'wallet_address' in request.session:
            del request.session['wallet_address']

        # Если есть другие флаги, относящиеся к подключению, их также можно удалить:
        if 'wallet_connected' in request.session:
            del request.session['wallet_connected']

        # Перенаправляем на главную страницу после отключения
        return HttpResponseRedirect(reverse('index'))


class WalletMoreInfoView(TemplateView):
    template_name = "wallet_analyzer/components/wallet_more_info.html"

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, есть ли кошелек в сессии; если нет — перенаправляем на подключение
        if 'wallet_address' not in request.session:
            return redirect('wallet_analyzer:wallet_connection')
        return super().dispatch(request, *args, **kwargs)

    def get_transaction_count(self, wallet_address):
        w3 = eth_connection.get_web3_instance()
        try:
            # Преобразуем адрес в формат контрольной суммы
            checksum_address = Web3.to_checksum_address(wallet_address)

            # Получаем количество транзакций
            tx_count = w3.eth.get_transaction_count(checksum_address)
            return tx_count
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet_address = self.request.session.get('wallet_address')

        # Получаем количество транзакций
        tx_count = self.get_transaction_count(wallet_address)

        # Передаем данные в контекст
        context['address'] = wallet_address
        context['tx_count'] = tx_count
        context['more_info'] = "Здесь может быть дополнительная информация о кошельке"

        return context

class NetworkInfoView(TemplateView):
    template_name = "wallet_analyzer/components/network_info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Создаем экземпляр EVMTools для сети Ethereum mainnet
        evm_tools = EVMTools("ethereum_mainnet")

        # Получаем цену газа и последний блок
        context['gas_price'] = evm_tools.get_gas_price()
        context['latest_block'] = evm_tools.get_latest_block()

        return context
class WalletAnalyzerView(TemplateView):
    template_name = "wallet_analyzer/index.html"


class WalletAnalyzerConnectionView(TemplateView):
    template_name = "wallet_analyzer/base.html"


class WalletAnalyzerCreateView(CreateView):
    model = Wallet
    form_class = WalletForm
