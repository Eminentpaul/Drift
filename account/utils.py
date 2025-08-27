from .models import Account, Transaction


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

    