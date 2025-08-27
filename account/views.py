from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import inflect


# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    inf = inflect.engine()

    user = request.user

    amount_words = inf.number_to_words(int(user.account.account_balance))

    context = {
        'amount_words': amount_words
    }
    return render(request, 'account/dashboard.html', context)
