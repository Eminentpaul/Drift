from django.db.models.signals import post_save
from .models import Account, DividendAccount





def create_account(sender, instance, created, **kwargs):
    if created:
        DividendAccount.objects.create(
            user=instance,
            account_id=instance.account_id,
            dividend=0
        )

# def save_account(sender, instance, **kwargs):
#     instance.account.save()

post_save.connect(create_account, sender=Account)
# post_save.connect(save_account, sender=Account)