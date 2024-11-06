from lib2to3.fixes.fix_input import context

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import Wallet

# Create your views here.


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