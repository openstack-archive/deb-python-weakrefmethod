from setuptools import setup
from codecs import open
from os import path
from weakrefmethod import __version__

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

URL = 'http://pypi.python.org/pypi/weakrefmethod'

setup(
    name='weakrefmethod',
    version=__version__,
    description='A WeakMethod class for storing bound methods using weak references.',
    long_description=long_description,
    py_modules=['weakrefmethod'],
    author='Tommy Wang',
    author_email='twang@august8.net',
    license='PSF',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='weakref WeakMethod',
    url='http://pypi.python.org/pypi/weakrefmethod',
    tests_require=['unittest2'],
    test_suite='test_weakmethod',
)
