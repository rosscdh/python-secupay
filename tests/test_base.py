# -*- coding: UTF-8 -*-
import pytest
from secupay import SecuPay

DEV_SETTINGS = {
    'DEBUG': True,
    'SECUPAY_DEBUG': True,
    'SECUPAY_TOKEN': '12345',
}

subject = SecuPay(settings=DEV_SETTINGS)


def test_payment_types():
    assert subject.payment_types().__class__.__name__ == 'PaymentTypes'
    assert subject.payment_types().uri == 'payment/gettypes'

    # Must not allow post
    with pytest.raises(Exception):
        subject.payment_types().post()


def test_payment():
    assert subject.payment().__class__.__name__ == 'Payment'
    assert subject.payment().uri == 'payment/init'


def test_payment_capture_preauthorized_payment():
    assert subject.payment().capture_preauthorized_payment(token='preauthtoken').__class__.__name__ == 'CapturePreAuthorizedPayment'
    assert subject.payment().capture_preauthorized_payment(token='preauthtoken').uri == 'payment/:hash/capture'


def test_payment_cancel_preauthorized_payment():
    assert subject.payment().cancel_preauthorized_payment(token='preauthtoken').__class__.__name__ == 'CancelPreAuthorizedPayment'
    assert subject.payment().cancel_preauthorized_payment(token='preauthtoken').uri == 'payment/:hash/cancel'
