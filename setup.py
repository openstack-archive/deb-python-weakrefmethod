import io
import os
from setuptools import setup, find_packages

version = io.open('weakrefmethod/_version.py',encoding='ascii').readlines()[-1].split()[-1].strip('"\'')

setup(
    name='weakrefmethod',
    version=version,
    description='A WeakMethod class for storing bound methods using weak references.',
    long_description=io.open('DESCRIPTION.rst', encoding='utf-8').read(),
    packages=find_packages(),
    include_package_data=True,
    url='http://github.com/twang817/weakrefmethod',
    download_url='https://github.com/twang817/weakrefmethod/tarball/{version}'.format(version=version),
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
    tests_require=['unittest2'],
    test_suite='test_weakmethod',
    extra_requires={
        'test': ["tox"]
    }
)
