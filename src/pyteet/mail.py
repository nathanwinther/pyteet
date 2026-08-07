from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import config
from .util import logger
from .util import parsebool
from .util import parseint

def send_mail(
        subject: str,
        body: str,
        to: str,
        cc: str | None=None,
        from_name:str | None=None,
        from_addr:str | None=None):
    if not isinstance(to, list):
        to = [to]

    if cc and not isinstance(cc, list):
        cc = [cc]

    cfg = config('mail')

    from_name = from_name if from_name else cfg.get('default_sender_name', '')
    from_addr = from_addr if from_addr else cfg.get('default_sender_addr', '')

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
        logger.debug('SMTP connect', extra=cfg)
        with SMTP(cfg('host'), parseint(cfg('port'))) as smtp:
            if parsebool(cfg('startssl', 'False')):
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
            smtp.login(cfg('username', ''), cfg('password', ''))
            smtp.send_message(msg)
    except Exception as e:
        logger.error(repr(e))
        raise e

