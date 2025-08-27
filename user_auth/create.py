from account.models import Account


def creatAccount(user, acctno, agent):
    return Account.objects.create(
        user=user,
        account_number=acctno,
        agent=agent
    )