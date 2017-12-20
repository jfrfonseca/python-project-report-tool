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
import os
from pprint import pprint

# Project
from python_project_report_tool import git_tools


"""
# CONFIG
"""


"""
# UTIL
"""


"""
# RUNTIME
"""


if __name__ == '__main__':
    print("Performing tests in ", os.getcwd())

    pprint(git_tools.count_commits_per_file())
