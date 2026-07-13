from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import config
from .log import Log
from .util import parsebool, parseint

def send_mail(subject, body, to, cc=None, from_name=None, from_addr=None):
    if not isinstance(to, list):
        to = [to]
    if cc and not isinstance(cc, list):
        cc = [cc]
    from_name = from_name if from_name else config('mail.default_sender_name', '')
    from_addr = from_addr if from_addr else config('mail.default_sender_addr', '')
    if not from_addr:
        raise ValueError('send_mail: from_addr required')
    from_addr = f'{from_name} <{from_addr}>' if from_name else from_addr
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ','.join(to)
    if cc:
        msg['Cc'] = ','.join(cc)
    msg.attach(MIMEText(body, 'html'))
    try:
        Log.debug('SMTP connect', **config('mail'))
        with SMTP(config('mail.host'), parseint(config('mail.port'))) as smtp:
            if parsebool(config('mail.startssl', 'False')):
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
            smtp.login(config('mail.username', ''), config('mail.password', ''))
            smtp.send_message(msg)
    except Exception as e:
        Log.error(repr(e))
        raise e

