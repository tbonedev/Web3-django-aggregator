

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, FormView

from .forms import WalletForm
from .models import Wallet
from .wallet_analysis.utils import EVMTools
from django.views import View


# Create your views here.
class WalletConnectView(FormView):
    template_name = 'wallet_analyzer/components/wallet_connection.html'
    form_class = WalletForm
    success_url = reverse_lazy('index')  # Перенаправление на главную страницу после успешной отправки формы

    def form_valid(self, form):
        wallet_address = form.cleaned_data['address']

        # Проверяем, существует ли уже адрес в базе данных
        wallet = Wallet.objects.filter(address=wallet_address).first()
        if not wallet:
            # Если адрес не существует, создаем новый объект
            wallet = Wallet.objects.create(address=wallet_address)

        # Сохраняем адрес кошелька в сессии
        self.request.session['wallet_address'] = wallet.address

        # Перенаправляем пользователя на success_url
        return super().form_valid(form)


class WalletBalanceView(TemplateView):
    template_name = "wallet_analyzer/components/wallet_balance.html"

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, есть ли кошелек в сессии; если нет — перенаправляем на подключение
        if 'wallet_address' not in request.session:
            return redirect('wallet_analyzer:wallet_connection')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем адрес кошелька из сессии
        wallet_address = self.request.session.get('wallet_address')

        # Подключаемся к сети и получаем баланс
        evm_tools = EVMTools("ethereum_mainnet")
        balance = evm_tools.get_balance(wallet_address)

        # Добавляем адрес и баланс кошелька в контекст
        context['address'] = wallet_address
        context['balance'] = balance

        return context


class WalletAnalyzerView(TemplateView):
    template_name = "wallet_analyzer/base_wallets.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wallets'] = Wallet.objects.all()
        return context



class WalletDisconnectView(View):
    def get(self, request):
        # Очистка сессии для удаления данных о кошельке
        if 'wallet_address' in request.session:
            del request.session['wallet_address']

        # Перенаправляем пользователя на главную страницу или страницу подключения кошелька
        return redirect('index')  # или укажите другую нужную страницу


class WalletAnalyzerListView(ListView):
    template_name = "wallet_analyzer/base_wallets.html"
    model = Wallet
    context_object_name = "wallets"


class WalletAnalyzerConnectionView(TemplateView):
    template_name = "wallet_analyzer/base.html"


class WalletAnalyzerCreateView(CreateView):
    model = Wallet
    form_class = WalletForm
