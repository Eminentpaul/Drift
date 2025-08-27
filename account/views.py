from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import inflect
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Transaction, Account
# from


# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    inf = inflect.engine()

    user = request.user

    agent_total_amount = 0

    agent_clients = Account.objects.all().filter(agent=request.user)


    for account in agent_clients:
        agent_total_amount += int(account.account_balance)


    if user.is_agent:
        amount_words = inf.number_to_words(int(agent_total_amount))
    else:
        amount_words = inf.number_to_words(int(user.account.account_balance))

    agent_transaction = Transaction.objects.all().filter(sender=user)


    context = {
        'amount_words': amount_words, 
        'agent_transaction': agent_transaction,
        'agent_total_amount': agent_total_amount,
    }
    return render(request, 'account/dashboard.html', context)
