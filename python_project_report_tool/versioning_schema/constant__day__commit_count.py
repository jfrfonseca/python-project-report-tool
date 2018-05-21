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


# This package
from python_project_report_tool.git_tools import parse_git_date


"""
# UTIL
"""


def __format_record__constant__day__commit_count(file_record, constant):
    date = parse_git_date(file_record['last_update'])
    return "{0}.{1}{2:02d}{3:02d}.{4}".format(constant, date.year, date.month, date.day, file_record['commits'])


def constant__day__commit_count(git_file_history, constant):
    return [__format_record__constant__day__commit_count(record, constant) for record in git_file_history]