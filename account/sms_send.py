from twilio.rest import Client
from .masking import mask
from django.conf import settings
from django.contrib import messages as mg
from django.shortcuts import redirect
from datetime import datetime




def send_sms(acctno, depamount, desc, acctbal, date, to='+18777804236'):
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN

    # Formating Date and Time
    format_code = "%d-%m-%Y %I:%M%p"
    datetime_object = datetime.fromisoformat(str(date)).strftime(format_code)


    # try:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='+13304815882',
        body=f"""\n
Acct: {mask(acctno)}
Amt: NGN{depamount}
Desc: {desc}
Avail Bal: NGN{acctbal}
Date: {datetime_object} """,
        to=to
    )

    # except Exception:
    #     pass 



# from twilio.rest import Client
# account_sid = 'AC97e57bf7d9a1612e1673e4cbacd35296'
# auth_token = '[AuthToken]'
# client = Client(account_sid, auth_token)
# message = client.messages.create(
#   messaging_service_sid='MGcf786649d9a2ec8dbfbbaf37619f12b2',
#   body=f"""Acct: ******5531
# Amt: NGN2000.00
# Desc: DEP FROM PAULINUS OSHI - ADS0089
# Avail Bal: NGN50,000.00
# Date: 2025""",
#   to='+18777804236'
# )
# print(message.sid)