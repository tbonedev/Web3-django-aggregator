
from django.urls import path

from . import views

app_name = "wallet_analyzer"

urlpatterns = [
    # path("", views.WalletAnalyzerView.as_view(), name="index"),
    path("", views.WalletAnalyzerView.as_view(), name="index"),
    path("wallets/", views.WalletAnalyzerListView.as_view(), name="wallet_list"),
    path("wallet/", views.WalletAnalyzerConnectionView.as_view(), name="wallet_connection"),
]
