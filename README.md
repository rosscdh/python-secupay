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

#
# Follow the url below, complete the process and copy the "code=:code_value" in the url
# this :code_value is then passed into the s.token_from_code(code=:code_value)
#
print s.auth_url
>>> 'https://app.secupay.com/oauth/authorize?scope=%2Foauth%2Fauthorize&redirect_uri=None&response_type=code&client_id=:your_client_id'

#
# complete the process at the above url which will result in a code being presented to you.
#

token = s.token_from_code(code=':code')

# you can also access the token via
s.access_token  # Will give you access to the token

#
# Use the token provided above to use the api in the following manner
#


from secupay.clio import Me
s = Me(session=s)
s.get()


from secupay.clio import Matters
s = Matters(session=s)
s.get()


#
# Create a matter
#
from secupay.clio import Matters
m = Matters(session=s)
m.post(client_id=882801947, description='a test matter', status='Open')


#
# Get single matter
#
from secupay.clio import Matters
m = Matters(session=s, id=1025003373)
m.get()


from secupay.clio import Documents
dd = Documents(session=s)
dd.get()


from secupay.clio import Documents
d = Documents(session=s, id=28745759)
d.document_versions()
d.download_version(version_id=30613503)

d.get()
v = d.version(version_id=30613503)

from secupay.clio import DocumentCategories
dc = DocumentCategories(session=s)
dc.get()


from secupay.clio import Contacts
c = Contacts(session=s)
c.get()

from secupay.clio import Notes
n = Notes(session=s)
n.get()

from secupay.clio import Activities
a = Activities(session=s)
a.get()

from secupay.clio import Bills
b = Bills(session=s)
b.get()
```

Pagination
----------

As per the secupay docs (http://api-docs.clio.com/v2/index.html#rest-api)

```
from secupay.clio import Matters
m = Matters(session=s)
next_page = m.get(next_offset=:next_offset_from_previous_json_response_aata)
```


To paginate and basically do anythign via GET params (as per secupay api docs) pass in the desired param arguments as keyword arguments i.e. "s.get(offset=2)".


ToDo
----

1. ~~Self contained session to provideo oauth2 token~~
2. ~~Examples of pagination and other api operators~~
3. Tests
