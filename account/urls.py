from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('recipient/', views.recipient, name='recipient'),
    path('transactions/', views.transactions, name='transactions'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
    path('clients/', views.clients, name='clients'),
    path('pin_verification/', views.pin, name='pin'),
    path('transaction/<str:pk>/details/', views.transaction_detail, name='transaction_detail'),
    path('client/<str:pk>/details/', views.client_detail, name='client_detail'),
]