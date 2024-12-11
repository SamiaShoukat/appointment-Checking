import os
import yagmail
from dotenv import load_dotenv

load_dotenv()
EMAIL=os.environ.get('SENDER_EMAIL')
PASS=os.environ.get('SENDER_PASS')

DEFAULT_SUBJECT = 'URGENT: Appointment Open!'
DEFAULT_CONTENT = 'New Appointment: https://service2.diplo.de/rktermin/extern/choose_realmList.do?locationCode=isla&request_locale=en \n Cancel Old Appointment: https://mail.google.com/mail/u/0/#search/diplo.de/FMfcgzGqRZXPdJGVVpMQhfsGWkVbcWxC'
def send_mail(subject = DEFAULT_SUBJECT, contents = DEFAULT_CONTENT):
    yag = yagmail.SMTP(EMAIL, PASS)
    yag.send(
        to=os.environ.get('RECVR_EMAILS').split(' '),
        subject=subject,
        contents=contents,
    )

if __name__ == '__main__':
    send_mail('Test Email', 'Test Content')
