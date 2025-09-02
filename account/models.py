from django.db import models
from user_auth.models import User
from shortuuid.django_fields import ShortUUIDField
from django.shortcuts import get_object_or_404
from .twillo import send_sms 
# from .utils import mask


# Create your models here.
ACCOUNT_STATUS = (
    ('active', 'Active'),
    ('in-active', 'In-Active')
)

STATUS = (
    ('Success', 'Success'),
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Cancelled', 'Cancelled'),
)


TRANSACTION_TYPE = (
    ('Deposit', 'Deposit'),
    ('Widthdrawal', 'Widthdrawal'),
    # ('Transfer', 'Transfer'),
)

class Account(models.Model):
    account_id = ShortUUIDField(
        unique=True, length=7, max_length=25, prefix='ADS', alphabet='1234567890')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    account_number = models.CharField(max_length=10)
    account_balance = models.DecimalField(
        max_length=12, decimal_places=2, max_digits=12, default=0.00)
    account_status = models.CharField(
        max_length=100, choices=ACCOUNT_STATUS, default='active')
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name='agent')
    date = models.DateTimeField(auto_now_add=True)
    set_amount = models.BooleanField(default=False)
    account_pin = models.IntegerField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    contributing_amount = models.DecimalField(max_length=12, default=0.00, max_digits=12, decimal_places=2)

    class Meta:
        ordering = ['-update']
        
    def __str__(self):
        return f"{self.account_id} | {self.account_number}"
    
    # def get_url(self):
    #     return reverse('deposit', args=[self.account_id])


class DividendAccount(models.Model):
    user = models.OneToOneField(Account, on_delete=models.SET_NULL, null=True)
    account_id = models.CharField(max_length=200)
    dividend = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    


class Transaction(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='sender')
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='receiver')
    amount = models.DecimalField(
        max_length=12, decimal_places=2, max_digits=12, default=0.00)
    transaction_status = models.CharField(max_length=20, choices=STATUS, default='Success')
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE, default='Deposit')
    ref_number = ShortUUIDField(
        unique=True, length=20, max_length=25, prefix='TRN-', alphabet='1234567890')
    withdraw_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sender}'
    

    def clean(self):
        if self.transaction_status == 'Approved' and \
            self.withdraw_approved == False and \
                self.transaction_type == 'Widthdrawal':
            
            account = get_object_or_404(Account, user=self.receiver)
            account.account_balance -= self.amount
            account.save()
            

            send_sms(
                    acctbal=account.account_balance,
                    acctno=account.account_number, 
                    depamount=self.amount,
                    desc=f'WITHDRAWAL by You, {self.receiver}',
                    date=self.updated
                )


            
            self.withdraw_approved = True
            return self.withdraw_approved


    class Meta:
        ordering = ['-created']


class All_User_Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user')
    user_id_number = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='transaction')
    checked = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'All User Transaction'
