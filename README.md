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
from django.conf import settings
from secupay import get_session, SecuPay

session = get_session(settings)

sp = SecuPay(session=session)

sp.payment_types().get()

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
