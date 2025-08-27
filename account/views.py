from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import inflect
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Transaction, Account
from .utils import All
from django.contrib import messages as mg


# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    inf = inflect.engine()

    user = request.user
    a = All(user)


    if user.is_agent:
        amount_words = inf.number_to_words(int(a.agent_total_amount()))
    else:
        amount_words = inf.number_to_words(int(user.account.account_balance))

    agent_transaction = Transaction.objects.all().filter(sender=user)
    user_transaction = Transaction.objects.all().filter(receiver=user)

    # Setting User Contributing Amount 
    if request.method == 'POST':
        amount = request.POST.get('amount')
        
        if int(amount) < 200:
            mg.error(request, 'The Contributing Amount should be N200 or above!')
        else:
            account = get_object_or_404(Account, user=request.user)
            account.contributing_amount = float(amount)
            account.set_amount = True
            account.save()

            return redirect('dashboard')


    context = {
        'amount_words': amount_words, 
        'agent_transaction': agent_transaction,
        'agent_total_amount': a.agent_total_amount(),
        'agent_clients': a.agent_client(), 
        'user_transaction': user_transaction
    }
    return render(request, 'account/dashboard.html', context)


def deposit(request):
    context = {
        'agent_total_amount': agent_total_amount(),
    }
    return render(request, 'account/deposit-money.html')