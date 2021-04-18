#!/usr/bin/python
# coding=utf-8

"""
Created on 2018年11月7日

@author: qyke
"""

import os
import time


class Log:

    @staticmethod
    def log_message(file_name, format='%s', *args):
        log_dir = os.path.abspath(os.path.dirname(__file__))
        log_dir = os.path.join(log_dir, '..', 'log', file_name)
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, file_name + '-{0}.log'.format(time.strftime("%Y-%m-%d", time.localtime())))
        with open(log_file, 'a+') as f:
            print("[%s] %s\n" % (Log.log_date_time_string(), format % args))
            f.write("[%s] %s\n" % (Log.log_date_time_string(), format % args))

    @staticmethod
    def log_date_time_string():
        """Return the current time formatted for logging."""
        now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
        s = "%02d/%02s/%04d %02d:%02d:%02d--------" % (
                day, month, year, hh, mm, ss)
        return s
