

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, FormView

from .forms import WalletForm
from .models import Wallet

# Create your views here.
class WalletConnectView(FormView):
    template_name = 'components/wallet_connection.html'
    form_class = WalletForm
    success_url = reverse_lazy('index')  # Перенаправление на главную страницу после успешной отправки формы

    def form_valid(self, form):
        wallet_address = form.cleaned_data['address']

        # Проверяем, существует ли уже адрес в базе данных
        if not Wallet.objects.filter(address=wallet_address).exists():
            # Сохраняем новый адрес
            Wallet.objects.create(address=wallet_address)

        # Выполняем перенаправление на success_url
        return super().form_valid(form)

class WalletAnalyzerView(TemplateView):
    template_name = "wallet_analyzer/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wallets'] = Wallet.objects.all()
        return context


class WalletAnalyzerListView(ListView):
    template_name = "wallet_analyzer/index.html"
    model = Wallet
    context_object_name = "wallets"


class WalletAnalyzerConnectionView(TemplateView):
    template_name = "wallet_analyzer/base.html"


class WalletAnalyzerCreateView(CreateView):
    model = Wallet
    form_class = WalletForm
