# -*- coding: UTF-8 -*-
from secupay import SecuPay

DEV_SETTINGS = {
    'DEBUG': True,
    'SECUPAY_DEBUG': True,
    'SECUPAY_TOKEN': '12345',
}

PROD_SETTINGS = DEV_SETTINGS.copy()
PROD_SETTINGS.update({
    'DEBUG': False,
    'SECUPAY_DEBUG': False,
})

sp_dev = SecuPay(settings=DEV_SETTINGS)
sp_prod = SecuPay(settings=PROD_SETTINGS)


def test_dev_settings():
    assert sp_dev.session.__class__.__name__ == 'DevelopmentSession'
    assert sp_dev.session.site == 'https://api-dist.secupay-ag.de/'
    assert sp_prod.session.token is '12345'
    assert sp_prod.session.language is 'en_US'
    assert sp_dev.session.debug is True
    assert sp_dev.session.demo is True


def test_prod_settings():
    assert sp_prod.session.__class__.__name__ == 'Session'
    assert sp_prod.session.site == 'https://api.secupay.ag/'
    assert sp_prod.session.token is '12345'
    assert sp_prod.session.language is 'en_US'
    assert sp_prod.session.debug is False
    assert sp_prod.session.demo is False


def test_prod_settings_with_demo_true():
    prod_settings = DEV_SETTINGS.copy()
    prod_settings.update({
        'DEBUG': False,
        'SECUPAY_DEBUG': True,
    })

    subject = SecuPay(settings=prod_settings)
    assert subject.session.__class__.__name__ == 'Session'
    assert subject.session.site == 'https://api.secupay.ag/'
    assert sp_prod.session.token is '12345'
    assert sp_prod.session.language is 'en_US'
    assert subject.session.debug is False
    assert subject.session.demo is True


def test_prod_settings_with_language_german():
    prod_settings = DEV_SETTINGS.copy()
    prod_settings.update({
        'DEBUG': False,
        'SECUPAY_DEBUG': True,
        'SECUPAY_LANGUAGE': 'de_DE',
    })

    subject = SecuPay(settings=prod_settings)
    assert subject.session.__class__.__name__ == 'Session'
    assert subject.session.site == 'https://api.secupay.ag/'
    assert subject.session.token is '12345'
    assert subject.session.language is 'de_DE'
    assert subject.session.debug is False
    assert subject.session.demo is True
