from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import inflect
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Transaction, Account, All_User_Transaction
from .utils import All, cipher
from django.contrib import messages as mg
from user_auth.validation import phone_number_validation
from django.db import transaction
from django.core.paginator import Paginator


# Create your views here.

inf = inflect.engine()

@login_required(login_url='login')
def dashboard(request):
    

    user = request.user
    a = All(user)
    

    if user.is_agent:
        amount_words = inf.number_to_words(int(a.agent_total_amount()))
    else:
        cipher(request.user)
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


@login_required(login_url='login')
def deposit(request):
    user = request.user
    a = All(user)
    phone = ''
    recipient = ''

    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')

        account = get_object_or_404(Account, account_number=phone_number_validation(phone))
        recipient = account.user.get_full_name

        if int(amount) % int(account.contributing_amount) == 0:
            with transaction.atomic():
                account.account_balance += int(amount)
                account.save()

                trans = Transaction.objects.create(
                    sender = request.user,
                    receiver = account.user,
                    amount = float(amount),
                    transaction_status = 'Success',
                    transaction_type = 'Deposit',
                )

                for amount in range(int(int(amount)/int(account.contributing_amount))):
                    All_User_Transaction.objects.create(
                        user = account.user,
                        user_id_number = account.account_id,
                        amount = account.contributing_amount,
                        transaction = trans
                    )

            mg.success(request, 'Money Deposited Successfully')
            return redirect('dashboard')
        else: mg.error(request, 'This Amount cannot go!')

    context = {
        'agent_total_amount': a.agent_total_amount(),
        'amount_words': inf.number_to_words(int(a.agent_total_amount())),
        'phone': phone,
        'recipient': recipient 
    }
    return render(request, 'account/deposit-money.html', context)


@login_required(login_url='login')
def recipient(request):
    phone = request.GET.get('phone')
    
    account_number = phone_number_validation(phone)

    recipient = get_object_or_404(Account, account_number=account_number)
    
    return render(request, 'account/includes/recipient.html', {'recipient': recipient.user.get_full_name})


@login_required(login_url='login')
def transactions(request, transaction=None):
    user = request.user
    a = All(user)

    if user.is_agent:
        transaction = Transaction.objects.all().filter(sender=user)
        amount_words = inf.number_to_words(int(a.agent_total_amount()))
    else:
        transaction = Transaction.objects.all().filter(receiver=user)
        amount_words = inf.number_to_words(int(user.account.account_balance))


    paginator = Paginator(transaction, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    

    context = {
        'agent_total_amount': a.agent_total_amount(),
        'amount_words': inf.number_to_words(int(a.agent_total_amount())),
        'page_obj': page_obj,
        'amount_words': amount_words,
    }
    return render(request, 'account/transactions.html', context)



@login_required(login_url='login')
def withdrawal(request):
    user = request.user
    a = All(user)
    total = 0
    all_transaction = All_User_Transaction.objects.all().filter(user_id_number=user.account.account_id, checked=True)

    for trans in all_transaction:
        total += int(float(trans.amount))


    if request.method == 'POST':
        amount = request.POST.get('amount')

        if int(amount) > total:
            mg.error(request, f'You can withdraw more than N{total}')
        else:
            Transaction.objects.create(
                sender = user,
                receiver = user,
                amount = int(amount), 
                transaction_status = 'Pending',
                transaction_type = 'Widthdrawal', 
            )
            mg.success(request, 'Your Widthdrawal has been placed successfully')
            
            return redirect('dashboard')


    context = {
        'agent_total_amount': a.agent_total_amount(),
        'amount_words': inf.number_to_words(int(user.account.account_balance)),
    }
    return render(request, 'account/withdraw-money.html', context)



@login_required(login_url='login')
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)
    
    context = {
        'transaction': transaction,
        'amount_words': inf.number_to_words(int(transaction.amount)),
    }
    return render(request, 'account/includes/transaction-detail.html', context)