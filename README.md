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
from secupay import get_session, SecuPay

sp = SecuPay(settings=settings)

sp.payment_types().get()  # List of payment types

sp.payment().post(example='test')
sp.payment().status().get()

sp.payment().cancel_preauthorized_payment(token='1234').get()
sp.payment().capture_preauthorized_payment(token='1234').get()
```

ToDo
----

1. ~~Self contained session to provid api token/key~~
2. Examples of pagination and other api operators
3. Tests
