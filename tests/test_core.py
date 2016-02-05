# -*- coding: UTF-8 -*-
from secupay import SecuPay

DEV_SETTINGS = {
    'SECUPAY_DEVELOPMENT': True,
    'SECUPAY_DEMO': True,
    'SECUPAY_TOKEN': '12345',
}

subject = SecuPay(settings=DEV_SETTINGS)


def test_wrap_namespace():
    """
    Test we have the correct data structure
    """
    resp = subject.payment().wrap_namespace(my='test', keywords='here')
    assert resp == '{"data": {"keywords": "here", "demo": 1, "apikey": "12345", "my": "test"}}'


def test_headers():
    assert subject.payment().headers() == {'Accept': 'application/json;', 'Content-Type': 'application/json; charset=utf-8;'}
