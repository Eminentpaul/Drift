from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages as mg
# from django.db.models import Q
# from django.contrib.auth.decorators import login_required
from .forms import UserRegistration
from .validation import phone_number_validation
from .models import User
from .create import creatAccount
# from account.models import Account, Transaction
# from _datetime import datetime
from django.utils import timezone




# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        phone = request.POST.get('phone')
        password = request.POST.get('password')

        new_number = f"0{phone_number_validation(phone)}"
       
        user = auth.authenticate(phone=new_number, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            mg.error(request, 'Invalid Phone Number or Password')

    return render(request, 'user_auth/login.html')


def registration(request):
    form = UserRegistration()
    error_msg = []
    if request.method == 'POST':
        phone = request.POST.get('phone')
        agent = request.POST.get('agent')

        password = request.POST.get('password1')
        cpassword = request.POST.get('password2')

        if cpassword != password:
            mg.error(request, 'The Passwords are not the same')

        if len(phone) < 11:
            mg.error(request, 'The Number digits should up to 11')

        try:
            check_agent = User.objects.get(user_id=agent)
            new_number = phone_number_validation(phone)

            check_user = User.objects.filter(phone=new_number)

            if check_user.exists():
                mg.error(request, 'The Phone Number has been used')
            else:
                form = UserRegistration(request.POST)

                if form.is_valid():
                    user_number = f'0{new_number}'
                    user = form.save(commit=False)
                    user.phone = user_number
                    user.save()



                    creatAccount(user, new_number, check_agent)
                    auth.login(request, user)

                    return redirect('dashboard')
                else:
                    errMsg = [(k, v[0]) for k, v in form.errors.items()]
                    mg.error(request, form.errors.as_text()[15:])

        except User.DoesNotExist:
            mg.error(request, 'Invalid Agent ID')

    context = {'form': form}
    return render(request, 'user_auth/register.html', context)


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')