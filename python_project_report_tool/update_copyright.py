#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
"""


__copyright__  = 'Copyright (c) 2018 José F. R. Fonseca'
__credits__    = []
__author__     = ''
__maintainer__ = ''
__date__       = ''
__version__    = ''


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
