#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
"""


__copyright__  = 'Copyright (c) 2018 José F. R. Fonseca'
__credits__    = []
__author__     = ''
__maintainer__ = ''
__date__       = '27/09/2018 21:49:38'
__version__    = '0.20180927.1'


"""
# IMPORTS
"""


# Standard Library
import re


"""
# PAYLOAD
"""


def update_copyright_message(file_path, copyright_message, copyright_tag_regex='__copyright__\s*=\s*', copyright_tag='__copyright__  = '):
    rgx = re.compile(copyright_tag_regex)

    with open(file_path, 'r') as fin:
        indata = fin.readlines()

    for i, line in enumerate(indata):
        if rgx.search(line):
            indata[i] = "{}'{}'\n".format(copyright_tag, copyright_message)
            with open(file_path, 'w') as fout:
                fout.writelines(indata)
            return True

    return False


def update_date(file_path, date, date_tag_regex='__date__\s*=\s*', date_tag='__date__       = '):
    rgx = re.compile(date_tag_regex)

    with open(file_path, 'r') as fin:
        indata = fin.readlines()

    for i, line in enumerate(indata):
        if rgx.search(line):
            indata[i] = "{}'{}'\n".format(date_tag, date)
            with open(file_path, 'w') as fout:
                fout.writelines(indata)
            return True

    return False


def update_version(file_path, version, version_tag_regex='__version__\s*=\s*', version_tag='__version__    = '):
    rgx = re.compile(version_tag_regex)

    with open(file_path, 'r') as fin:
        indata = fin.readlines()

    for i, line in enumerate(indata):
        if rgx.search(line):
            indata[i] = "{}'{}'\n".format(version_tag, version)
            with open(file_path, 'w') as fout:
                fout.writelines(indata)
            return True

    return False
