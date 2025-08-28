from django.contrib import admin
from .models import Account, Transaction, All_User_Transaction, DividendAccount
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_id', 'user', 'account_number',
                    'account_balance', 'account_status', 'agent']
    list_display_links = ['account_id', 'user', 'account_number',
                    'account_balance', 'account_status', 'agent']
    search_fields = ['account_number']

    list_per_page = 20
    
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'amount',
                    'transaction_status', 'ref_number', 'created']
    list_display_links = ['sender', 'receiver', 'amount', 'ref_number', ]
    search_fields = ['amount', 'receiver__first_name',
                     'receiver__last_name', 'ref_number']
    list_editable = ['transaction_status']
    list_filter = ['transaction_type']

    list_per_page = 20
    
class AllTransAdmin(admin.ModelAdmin):
    list_display = ['user_id_number', 'user', 'amount', 'transaction', 'checked']
    list_display_links = ['user_id_number', 'user', 'amount', 'transaction', 'checked']
    search_fields = ['user_id_number']
    list_filter = ['user', 'checked']
    list_per_page = 35


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(All_User_Transaction, AllTransAdmin)  
admin.site.register(DividendAccount) 