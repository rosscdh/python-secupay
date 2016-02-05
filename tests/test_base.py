# -*- coding: UTF-8 -*-
import json
import pytest
import httpretty

from secupay import SecuPay

DEV_SETTINGS = {
    'SECUPAY_DEVELOPMENT': True,
    'SECUPAY_DEMO': True,
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


@httpretty.activate
def test_make_payment():
    expected_response = {
        "status": "ok",
        "data": {
            "hash": "tujevzgobryk3303",
            "iframe_url": "https://api.secupay.ag/payment/tujevzgobryk3303"
        },
        "errors": None
    }

    httpretty.register_uri(httpretty.POST, "https://api-dist.secupay-ag.de/payment/init",
                           body=json.dumps(expected_response),
                           content_type="application/json")

    payment = subject.payment()

    response = payment.make_payment(amount=25.00,
                                    payment_type='debit',
                                    url_success='http://localhost/payment/success/',
                                    url_failure='http://localhost/payment/fail/',
                                    url_push='http://localhost/payment/status/')

    assert response == expected_response

    expected_posted_data = {'amount': 2500,
                            'labels': {'de_DE': {'basket_title': 'Ihre Bestellung',
                                                 'cancel_button_title': 'Zum Warenkorb',
                                                 'submit_button_title': 'Daten Ubermitteln'},
                                       'en_US': {'basket_title': 'Your Order',
                                                 'cancel_button_title': 'Return to Basket',
                                                 'submit_button_title': 'Submit'}},
                            'payment_type': 'debit',
                            'url_failure': 'http://localhost/payment/fail/',
                            'url_push': 'http://localhost/payment/status/',
                            'url_success': 'http://localhost/payment/success/'}

    assert payment.send_data == expected_posted_data


def test_payment_capture_preauthorized_payment():
    assert subject.payment().capture_preauthorized_payment(token='preauthtoken').__class__.__name__ == 'CapturePreAuthorizedPayment'
    assert subject.payment().capture_preauthorized_payment(token='preauthtoken').uri == 'payment/:hash/capture'


def test_payment_cancel_preauthorized_payment():
    assert subject.payment().cancel_preauthorized_payment(token='preauthtoken').__class__.__name__ == 'CancelPreAuthorizedPayment'
    assert subject.payment().cancel_preauthorized_payment(token='preauthtoken').uri == 'payment/:hash/cancel'
