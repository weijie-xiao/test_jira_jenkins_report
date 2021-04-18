#!/usr/bin/python
# coding=utf-8
"""
Created on 2019年05月05日
@author: qyke

"""

from setuptools import find_packages, setup

setup(
    name="auto_test_weekly_report",
    version="1.1",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=["auto_report/bin/report"],
    install_requires=["requests",
                      "requests_html",
                      "jira==2.0.0"]
)

# 如果安装jira 2.0.0报错 cryptography  'openssl/opensslv.h': No such file or directory ，\
# 请看 https://stackoverflow.com/questions/45089805/pip-install-cryptography-in-windows/45089806
