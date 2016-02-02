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

sp.payment_types().get()  # List of payment types

sp.payment().post(example='test')
sp.payment().status().get()

sp.payment().cancel_preauthorized_payment(token='1234').get()
sp.payment().capture_preauthorized_payment(token='1234').get()
```



## Tests

We use py.test

```
py.test                                                                                                  rosscdh@s
================================================ test session starts ================================================
platform darwin -- Python 2.7.5, pytest-2.8.7, py-1.4.31, pluggy-0.3.1
rootdir: /Users/rosscdh/p/stefano/vendors/python-secupay, inifile:
collected 8 items

tests/test_base.py ....
tests/test_session.py ....

============================================= 8 passed in 0.10 seconds ==============================================
```

ToDo
----

1. ~~Self contained session to provid api token/key~~
2. Examples of pagination and other api operators
3. Tests
