from setuptools import setup

setup(
    name="python-secupay",
    packages=['secupay'],
    version='0.0.1',
    author="Ross Crawford-d'Heureuse",
    license="MIT",
    author_email="sendrossemail@gmail.com",
    url="https://github.com/rosscdh/python-secupay",
    description="A python module for using the secupay api",
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'requests',
        'pytest',
        'coverage',
        'httpretty',
    ]
)
