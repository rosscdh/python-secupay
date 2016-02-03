# -*- coding: UTF-8 -*-
from .secupay import DevelopmentSession, Session
from .secupay import BaseApi, Payment, PaymentTypes


def get_session(settings):
    if type(settings) is dict:
        debug = settings.get('DEBUG', True)
        secupay_debug = settings.get('SECUPAY_DEBUG', True)
        language = settings.get('SECUPAY_LANGUAGE', 'en_US')
        token = settings.get('SECUPAY_TOKEN', None)
    else:
        debug = getattr(settings, 'DEBUG', True)
        secupay_debug = getattr(settings, 'SECUPAY_DEBUG', True)
        language = getattr(settings, 'SECUPAY_LANGUAGE', 'en_US')
        token = getattr(settings, 'SECUPAY_TOKEN', None)

    SECUPAY_LABELS = getattr(settings, 'SECUPAY_LABELS', {
        "en_US": {
            "basket_title": "Your Order",
            "submit_button_title": "Submit",
            "cancel_button_title": "Return to Basket"
        },
        "de_DE": {
            "basket_title": "Ihre Bestellung",
            "submit_button_title": "Daten Ubermitteln",
            "cancel_button_title": "Zum Warenkorb"
        }
    })

    assert token is not None, 'You must provide a SECUPAY_TOKEN in the settings passed into secupay.get_session(settings)'

    if debug is False:

        return Session(token=token,
                       debug=debug,
                       secupay_debug=secupay_debug,
                       language=language,
                       SECUPAY_LABELS=SECUPAY_LABELS)

    return DevelopmentSession(token=token,
                              debug=debug,
                              secupay_debug=secupay_debug,
                              language=language,
                              SECUPAY_LABELS=SECUPAY_LABELS)


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
