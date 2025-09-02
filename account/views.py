from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import inflect
from user_auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Transaction, Account, All_User_Transaction
from .utils import All, cipher
from .masking import mask
from django.contrib import messages as mg
from user_auth.validation import phone_number_validation
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
import json
from .forms import UserUpdateForm
from .twillo import send_sms


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
        pin = request.POST.get('pin')
        
        if int(amount) < 200:
            mg.error(request, 'The Contributing Amount should be N200 or above!')

        if len(pin) < 4 or len(pin) > 4:
            mg.error(request, 'Your PIN number should 4 inputs')

        if pin == '1234':
            mg.error(request, f'The PIN ({pin}) is simple!')
        else:
            account = get_object_or_404(Account, user=request.user)
            account.contributing_amount = float(amount)
            account.account_pin = pin
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
def profile(request, pk):
    user = request.user
    a = All(user)
    error_msg = []

    if user.is_agent:
        amount_words = inf.number_to_words(int(a.agent_total_amount()))
    else: 
        amount_words = inf.number_to_words(int(user.account.account_balance))

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        address = request.POST.get('address')

        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            print(form)
            user_detail = form.save(commit=False)
            user_detail.first_name = first_name
            user_detail.last_name = last_name
            user_detail.gender = gender
            user_detail.dob = dob
            user_detail.address = address
            
            user_detail.save()
        else: 
            errors = form.errors.get_json_data(escape_html=True)
            for error in errors:
                error_msg = errors[error][0]['message']

            mg.error(request, error_msg)


    context = {
        'amount_words': amount_words,
        'agent_total_amount': a.agent_total_amount(),
        'account_number': mask(acctno=user.account.account_number)
    }
    return render(request, 'account/profile.html', context) 


@login_required(login_url='login')
def edit_profile(request, pk):
    user = request.user
    a = All(user)
    
    
    
    return render(request, 'account/includes/edit-profile.html') 


@login_required(login_url='login')
def pin_pop(request, pk):
    
    mg.warning(request, 'ENTER YOUR CORRECT CURRENT PIN')      

    return render(request, 'account/includes/change-pin.html')


@login_required(login_url='login')
def pin_change(request, pk):
    user = get_object_or_404(User, user_id=pk)
    
    if request.method == 'POST':
        pin = request.POST.get('current_pin')
        new_pin = request.POST.get('new_pin')
        c_pin = request.POST.get('confirm_pin')

        if str(user.account.account_pin) == pin:
            if c_pin == new_pin:
                account = get_object_or_404(Account, account_id=user.account.account_id) 
                account.account_pin = new_pin
                account.save()

                mg.success(request, 'PIN UPDATED')
                return redirect('profile', user.user_id)
            else:
                mg.error(request, 'The New PIN and Confirm PIN is not the same!')

            
        else:
            mg.error(request, 'Enter your Correct CURRENT PIN')

    return render(request, 'account/includes/change-pin.html')



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
            instace = json.dumps({
                'amount': amount,
                'phone': phone
            })

            request.session['transact'] = instace 
            return redirect('pin')
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
    all_transaction = All_User_Transaction.objects.all().filter(user_id_number=user.account.account_id, checked=False)

    for trans in all_transaction:
        total += int(float(trans.amount))


    if request.method == 'POST':
        amount = request.POST.get('amount')

        if int(amount) > user.account.account_balance - total:
            mg.error(request, f'You can withdraw more than N{user.account.account_balance - total}')
        else:
            instace = json.dumps({
                'amount': amount,
            })

            request.session['transact'] = instace 
            return redirect('pin')
            


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


@login_required(login_url='login')
def clients(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    user = request.user
    a = All(user)

    account = Account.objects.filter(
        Q(account_id__icontains=q)|
        Q(user__last_name__icontains=q)|
        Q(user__phone__icontains=q)|
        Q(user__first_name__icontains=q)
    )


    paginator = Paginator(account, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'amount_words': inf.number_to_words(int(a.agent_total_amount())),
        'agent_total_amount': a.agent_total_amount(),
    }
    return render(request, 'account/clients.html', context)


@login_required(login_url='login')
def client_detail(request, pk):
    account = get_object_or_404(Account, id=pk)

    context = {
        'account': account,
        'amount_words': inf.number_to_words(int(account.account_balance)),
    }
    return render(request, 'account/includes/client-detail.html', context)



@login_required(login_url='login')
def pin(request):

    instance = request.session['transact']
    data = json.loads(instance)
    
    user = request.user

    if request.method == 'POST':
        pin = request.POST.get('pin') 

        if str(request.user.account.account_pin) == str(pin):
                        
            if user.is_agent:
                phone = data['phone']
                amount = data['amount']

                account = get_object_or_404(Account, account_number=phone_number_validation(phone))

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
                    transaction.on_commit(
                        lambda:send_sms(
                            depamount=data['amount'], 
                            acctbal=account.account_balance, 
                            desc=f'DEPOSIT from {user.account.agent}',
                            acctno=account.account_number,
                            date=trans.created
                        )
                    )

                    mg.success(request, 'Money Deposited Successfully')
                    return redirect('dashboard')

            else:
                amount = data['amount']

                Transaction.objects.create(
                    sender = user.account.agent,
                    receiver = user,
                    amount = int(amount), 
                    transaction_status = 'Pending',
                    transaction_type = 'Widthdrawal',
                )
                mg.success(request, 'Your Widthdrawal has been placed successfully')
                
                return redirect('dashboard')

    return render(request, 'account/pin.html') 