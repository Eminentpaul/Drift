from .models import Account, Transaction, All_User_Transaction
from django.shortcuts import get_object_or_404
from django.db import transaction


class All:
    def __init__(self, agent):
        self.agent = agent


    def agent_client(self):
        return Account.objects.all().filter(agent=self.agent)


    def agent_total_amount(self):
        agent_total_amount = 0

        for account in Account.objects.all().filter(agent=self.agent):
            agent_total_amount += int(account.account_balance)
        

        return agent_total_amount
    

 



def cipher(user):
    transactions = All_User_Transaction.objects.all().filter(user=user, checked=False)
    count_list = []

    for trans in transactions:
        count_list.append(trans)

        if len(count_list) == 31:
            # Deducting the contributing amount after 31 counts 
            account = get_object_or_404(Account, user=user)
            account.account_balance -= account.contributing_amount
            account.save()

            for count in count_list:
                count.checked = True 
                count.save()




def mask(user):
    prefix = user.account.account_number[:2]
    suffix = user.account.account_number[-2:]

    return f'{prefix}{'*' * 6}{suffix}'