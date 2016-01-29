# -*- coding: UTF-8 -*-
from .secupay import DevelopmentSession, Session
from .secupay import BaseApi, Payment, PaymentTypes


def get_session(settings):
    secupay_debug = getattr(settings, 'SECUPAY_DEBUG', True)
    token = getattr(settings, 'SECUPAY_TOKEN', None)

    self assert token, 'You must provide a SECUPAY_TOKEN in the settings passed into secupay.get_session(settings)'

    if settings.DEBUG is False and secupay_debug is False:
        return Session(token=token)
    return DevelopmentSession(token=token)


class SecuPay(BaseApi):
    """
    Generic wrapper object, to access the complex underlying object
    """
    def payment_types(self, **kwargs):
        return PaymentTypes(session=self.session)

    def payment(self, **kwargs):
        return Payment(session=self.session, **kwargs)
