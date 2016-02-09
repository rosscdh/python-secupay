python-secupay
=============

(in-development) Python Client for Secupay.ag


Installation
------------

```
git clone https://github.com/rosscdh/python-secupay.git
cd python-secupay
python setup.py install
```


## Basic Usage

```
#
# settings should be a dict object or have an implementation of
# getattr and provide the following
#
# DEBUG = True            ## Means a Development Session
# SECUPAY_DEBUG = True    ## Means demo = 1 sent to secupay regardless of environment
# SECUPAY_TOKEN = '<string api from the secupay website>'
#
from django.conf import settings
from secupay import SecuPay

sp = SecuPay(settings=settings)

sp.payment_types()  # List of payment types

# Make a Payment

# Create or have an existing local payment object that you have created in your database
payment = Payment.objects.get(uuid='1234-1234-1234-1234')

# Make the payment request
# Values here are from the "payment" model above

resp = sp.payment().make_payment(amount=25.00,
                                 payment_type='debit',
                                 url_success='http://localhost/payment/1234-1234-1234-1234/success/',
                                 url_failure='http://localhost/payment/1234-1234-1234-1234/fail/',
                                 url_push='http://localhost/payment/1234-1234-1234-1234/status/')
# Response from secupay
# {
#     "status": "ok",
#     "data": {
#             "hash": "tujevzgobryk3303",
#             "iframe_url": "https://api.secupay.ag/payment/tujevzgobryk3303"
#     },
#     "errors": null
# }

payment.secupay_hash = resp['data'].get('hash')  # tujevzgobryk3303 in this case
payment.iframe_url = resp['data'].get('iframe_url')  # https://api.secupay.ag/payment/tujevzgobryk3303 in this case
payment.save

#
# Show user the iframe
#

sp.payment().status().post(hash=':hash_of_payment_object')

sp.payment().cancel_preauthorized_payment(token='1234').get()
sp.payment().capture_preauthorized_payment(token='1234').get()
```



## Tests

We use py.test

```
py.test -vvv                                                                                                                                                                                                                      rosscdh@s
============================================================================================================ test session starts =============================================================================================================
platform darwin -- Python 2.7.5, pytest-2.8.7, py-1.4.31, pluggy-0.3.1 -- /Users/rosscdh/.virtualenvs/elbow/bin/python
cachedir: .cache
rootdir: /Users/rosscdh/p/s/vendors/python-secupay, inifile:
collected 11 items

tests/test_base.py::test_make_payment <- ../../../../.virtualenvs/elbow/lib/python2.7/site-packages/httpretty/core.py PASSED
tests/test_base.py::test_payment_types PASSED
tests/test_base.py::test_payment PASSED
tests/test_base.py::test_payment_capture_preauthorized_payment PASSED
tests/test_base.py::test_payment_cancel_preauthorized_payment PASSED
tests/test_core.py::test_wrap_namespace PASSED
tests/test_core.py::test_headers PASSED
tests/test_session.py::test_dev_settings PASSED
tests/test_session.py::test_prod_settings PASSED
tests/test_session.py::test_prod_settings_with_demo_true PASSED
tests/test_session.py::test_prod_settings_with_language_german PASSED

========================================================================================================= 11 passed in 0.25 seconds =========================================================================================================
```

ToDo
----

1. ~~Self contained session to provid api token/key~~
2. Examples of pagination and other api operators
3. Tests
