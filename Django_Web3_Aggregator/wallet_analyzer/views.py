from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, FormView
from django.views import View
from .forms import WalletForm
from .models import Wallet
from .wallet_analysis.utils import EVMTools


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
        if 'wallet_address' not in request.session:
            return HttpResponseRedirect(reverse_lazy('index'))  # Перенаправляем на главную страницу
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet_address = self.request.session.get('wallet_address')
        evm_tools = EVMTools("ethereum_mainnet")
        balance = evm_tools.get_balance(wallet_address)
        context['address'] = wallet_address
        context['balance'] = balance
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet_address = self.request.session.get('wallet_address')

        # Здесь добавьте логику получения дополнительной информации
        # Например:
        context['address'] = wallet_address
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
