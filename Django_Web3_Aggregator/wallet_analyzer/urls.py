from django.http import HttpResponse
from django.urls import path

from . import views

app_name = "wallet_analyzer"

urlpatterns = [
    path("", views.WalletAnalyzerView.as_view(), name="index"),
    path('wallet-connection/', views.WalletConnectView.as_view(), name="wallet_connect"),
    path('disconnect/', views.WalletDisconnectView.as_view(), name='wallet_disconnect'),
    path('balance/', views.WalletBalanceView.as_view(), name='wallet_balance'),
    path("wallet/", views.WalletAnalyzerConnectionView.as_view(), name="wallet_connection"),
]
