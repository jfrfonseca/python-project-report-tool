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
import sys
from pprint import pprint

# PIP
import pandas as pd

# Project
from python_project_report_tool import git_tools


"""
# CONFIG
"""


"""
# RUNTIME
"""

if __name__ == '__main__':
    if len(sys.argv) < 2:
        root_directory = os.getcwd()
    else:
        root_directory = sys.argv[1]
    history = git_tools.get_git_history(root_directory)
    df = pd.DataFrame(list(git_tools.get_file_history(history).values()))
    df = df[df['current']][[
        'path', 'filename', 'commits', 'last_update', 'maintainer', 'creation', 'author', 'credits',
    ]].sort_values(['path', 'filename']).to_excel("teste.xlsx", index=False)
