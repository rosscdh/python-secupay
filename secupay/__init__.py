# -*- coding: UTF-8 -*-
from .secupay import DevelopmentSession, Session
from .secupay import BaseApi, Payment, PaymentTypes
from .utils import get_namedtuple_choices


def get_session(settings):
    if type(settings) is dict:
        is_development = settings.get('SECUPAY_DEVELOPMENT', True)
        is_demo = settings.get('SECUPAY_DEMO', True)
        language = settings.get('SECUPAY_LANGUAGE', 'en_US')
        token = settings.get('SECUPAY_TOKEN', None)
    else:
        is_development = getattr(settings, 'SECUPAY_DEVELOPMENT', True)
        is_demo = getattr(settings, 'SECUPAY_DEMO', True)
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

    if is_development is False:

        return Session(token=token,
                       is_development=False,
                       is_demo=is_demo,
                       language=language,
                       SECUPAY_LABELS=SECUPAY_LABELS)

    return DevelopmentSession(token=token,
                              is_development=True,
                              is_demo=is_demo,
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
        return PaymentTypes(session=self.session).post()

    def payment(self, **kwargs):
        return Payment(session=self.session, **kwargs)

    def status_id_description(self, status_id):
        return SECUPAY_STATUS_CODES.get_desc_by_value(status_id)


SECUPAY_STATUS_CODES = get_namedtuple_choices('SECUPAY_STATUS_CODES', (
    ('1', 'code_0001', 'Invalid apikey',),
    ('2', 'code_0002', 'Invalid hash',),
    ('3', 'code_0003', 'Cannot capture unauthorized payment',),
    ('4', 'code_0004', 'Cannot cancel/void unaccepted payment',),
    ('5', 'code_0005', 'Invalid amount',),
    ('6', 'code_0006', 'Cannot refund unaccepted payment',),
    ('7', 'code_0007', 'No payment type available',),
    ('8', 'code_0008', 'Hash has already been processed',),
    ('9', 'code_0009', 'Scoring invalid',),
    ('10', 'code_0010', 'Payment denied by Scoring',),
    ('11', 'code_0011', 'Payment couldnt be finalized',),
    ('12', 'code_0012', 'Selected payment type is not available',),
    ('13', 'code_0013', 'Apikey mismatch',),
    ('14', 'code_0014', 'Cannot capture specified payment',),
    ('15', 'code_0015', 'Cannot cancel/void specified payment',),
    ('16', 'code_0016', 'Cannot refund specified payment',),
    ('17', 'code_0017', 'Invalid Paymentdata',),
    ('18', 'code_0018', 'Missing Parameter',),
    ('19', 'code_0019', 'Couldnt create the user',),
    ('20', 'code_0020', 'Username/email unavailable',),
    ('21', 'code_0021', 'Username or password invalid',),
    ('22', 'code_0022', 'Userauth Token invalid',),
    ('23', 'code_0023', 'Could not connect the card to the user',),
    ('24', 'code_0024', 'Invalid value for parameter',),
    ('25', 'code_0025', 'Cannot process specified payment',),
    ('26', 'code_0026', 'Cannot create payment information',),
    ('27', 'code_0027', 'Invalid data',),
    ('28', 'code_0028', 'Payment Provider declined the payment',),
    ('29', 'code_0029', 'No transaction available for this terminal',),
    ('30', 'code_0030', 'Cannot create transaction',),
    ('31', 'code_0031', 'Unknown parking zone',),
    ('32', 'code_0032', 'The password you entered is too short',),
    ('33', 'code_0033', 'The passwords are not equal',),
    ('34', 'code_0034', 'The data provided is not sufficient',),
    ('35', 'code_0035', 'There was an error creating the Apikey',),
    ('36', 'code_0036', 'The Plate is not valid',),
    ('37', 'code_0037', 'Payment data missing',),
    ('38', 'code_0038', 'Cannot find any active ticket for this zone and car',),
))
