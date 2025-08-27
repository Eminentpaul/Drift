from django.contrib import admin
from .models import Account, Transaction
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_id', 'user', 'account_number',
                    'account_balance', 'account_status', 'agent']
    search_fields = ['account_number']
    
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'amount',
                    'transaction_status', 'ref_number', 'created']
    list_display_links = ['sender', 'receiver', 'amount', 'ref_number', ]
    search_fields = ['amount', 'receiver__first_name',
                     'receiver__last_name', 'ref_number']

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)