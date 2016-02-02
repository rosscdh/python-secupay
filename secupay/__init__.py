# -*- coding: UTF-8 -*-
from .secupay import DevelopmentSession, Session
from .secupay import BaseApi, Payment, PaymentTypes


def get_session(settings):
    debug = getattr(settings, 'DEBUG', settings.get('DEBUG', True))
    secupay_debug = getattr(settings, 'SECUPAY_DEBUG', settings.get('SECUPAY_DEBUG', True))
    language = getattr(settings, 'SECUPAY_LANGUAGE', settings.get('SECUPAY_LANGUAGE', 'en_US'))

    token = getattr(settings, 'SECUPAY_TOKEN', settings.get('SECUPAY_TOKEN', None))

    assert token is not None, 'You must provide a SECUPAY_TOKEN in the settings passed into secupay.get_session(settings)'

    if debug is False:

        return Session(token=token,
                       debug=debug,
                       secupay_debug=secupay_debug,
                       language=language)

    return DevelopmentSession(token=token,
                              debug=debug,
                              secupay_debug=secupay_debug,
                              language=language)


class SecuPay(BaseApi):
    """
    Generic wrapper object, to access the complex underlying object
    """
    def __init__(self, settings):
        self.settings = settings
        self.session = get_session(self.settings)

    def payment_types(self):
        return PaymentTypes(session=self.session)

    def payment(self, **kwargs):
        return Payment(session=self.session, **kwargs)
