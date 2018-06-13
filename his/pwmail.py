"""Password mailing."""

from emaillib import EMail, Mailer

from his.config import CONFIG

__all__ = ['mail_password_reset_link']


PWRESET_CFG = CONFIG['pwreset']
MAIL_CFG = CONFIG['mail']

MAILER = Mailer(
    MAIL_CFG['server'], int(MAIL_CFG['port']), MAIL_CFG['user'],
    MAIL_CFG['passwd'])


def mail_password_reset_link(password_reset_token):
    """Mails the respective password reset link."""

    with open(PWRESET_CFG['template']) as file:
        template = file.read()

    account = password_reset_token.account
    link = PWRESET_CFG['link'].format(password_reset_token.token)
    html = template.format(account=account.name, link=link)
    email = EMail(
        PWRESET_CFG['subject'], MAIL_CFG['sender'], account.email,
        html=html)
    email.add_header('reply-to', PWRESET_CFG['reply_to'])
    MAILER.send([email])
    return True
