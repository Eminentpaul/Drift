from .models import Account, All_User_Transaction, DividendAccount
from django.shortcuts import get_object_or_404
from django.db import transaction
from .twillo import send_sms

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
    transactions = All_User_Transaction.objects.all().filter(user=user)
    count_list = []

    for trans in transactions:
        if trans.checked == True:
            # Deleting the Checked transaction 
            trans.delete()
            # trans.save()
        else:
            count_list.append(trans)

            if len(count_list) == 31:
                # Deducting the contributing amount after 31 counts 
                account = get_object_or_404(Account, user=user)
                account.account_balance -= account.contributing_amount
                account.save()

                # Registering the deducted Dividend
                dividend = get_object_or_404(DividendAccount, user=account)
                dividend.dividend += account.contributing_amount
                dividend.save()

                # Sending an Sms for collecting Dividend
                send_sms(
                    acctbal=account.account_balance,
                    acctno=account.account_number, 
                    depamount=account.contributing_amount,
                    desc='Monthly Contr. Chrge',
                    date=dividend.date
                )

                # Keeping Track of the collected Dividend 
                for count in count_list:
                    count.checked = True 
                    count.save()





