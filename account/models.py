from django.db import models
from user_auth.models import User
from shortuuid.django_fields import ShortUUIDField
from django.urls import reverse

# Create your models here.
ACCOUNT_STATUS = (
    ('active', 'Active'),
    ('in-active', 'In-Active')
)

STATUS = (
    ('Success', 'Success'),
    ('Pending', 'Pending'),
    ('Failed', 'Failed'),
)


TRANSACTION_TYPE = (
    ('Deposit', 'Deposit'),
    ('Widthdrawal', 'Widthdrawal'),
    # ('Transfer', 'Transfer'),
)

class Account(models.Model):
    account_id = ShortUUIDField(
        unique=True, length=7, max_length=25, prefix='ADS', alphabet='1234567890')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10)
    account_balance = models.DecimalField(
        max_length=12, decimal_places=2, max_digits=12, default=0.00)
    account_status = models.CharField(
        max_length=100, choices=ACCOUNT_STATUS, default='active')
    agent = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='agent')
    date = models.DateTimeField(auto_now_add=True)
    set_amount = models.BooleanField(default=False)
    account_pin = models.IntegerField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    contributing_amount = models.DecimalField(max_length=12, max_digits=12, default=200.00, decimal_places=2)

    class Meta:
        ordering = ['-update']
        
    def __str__(self):
        return f"{self.user.first_name}"
    
    def get_url(self):
        return reverse('deposit', args=[self.account_id])


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
    counts = models.CharField(max_length=20, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}'

    class Meta:
        ordering = ['-created']
