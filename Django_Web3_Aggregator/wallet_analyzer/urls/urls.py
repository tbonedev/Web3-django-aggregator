from django.http import HttpResponse
from django.urls import path

from wallet_analyzer import views

app_name = "wallet_analyzer"

urlpatterns = [
    path("", views.WalletAnalyzerView.as_view(), name="index"),
    path('wallet-connection/', views.WalletConnectView.as_view(), name="wallet_connect"),
    path('disconnect/', views.WalletDisconnectView.as_view(), name='wallet_disconnect'),
    path('balance/', views.WalletBalanceView.as_view(), name='wallet_balance'),
    path("wallet/", views.WalletAnalyzerConnectionView.as_view(), name="wallet_connection"),
    path('network_info/', views.NetworkInfoView.as_view(), name='network_info'),
    path('more_info/', views.WalletMoreInfoView.as_view(), name='wallet_more_info'),

]
