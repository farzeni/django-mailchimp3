#!/usr/bin/env python

from setuptools import setup, find_packages
import mailchimp3

setup(
    name='django-mailchimp3',
    version=".".join(map(str, mailchimp3.__version__)),
    author='Fabrizio Arzeni',
    author_email='fabrizio.arzeni@metadonors.it',
    url='http://github.com/metaforge/django-mailchimp3',
    install_requires=[
        'requests',
    ],
    description='Django package that deals with Mailchimp API v3.0',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)
