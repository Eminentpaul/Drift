from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('recipient/', views.recipient, name='recipient'),
    path('transactions/', views.transactions, name='transactions'),
]