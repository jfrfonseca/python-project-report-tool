#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
"""


__copyright__  = ''
__credits__    = []
__author__     = ''
__maintainer__ = ''
__date__       = ''
__version__    = ''


"""
# IMPORTS
"""


# Standard Library
import fileinput


"""
# PAYLOAD
"""


def update_copyright_message(file_path, copyright_message, copyright_tag='__copyright__  = '):

    for line in fileinput.input(file_path, inplace=True):
        if line.startswith(copyright_tag):
            line.replace(copyright_tag, copyright_tag + "'{}'".format(copyright_message))
            return True
    return False
