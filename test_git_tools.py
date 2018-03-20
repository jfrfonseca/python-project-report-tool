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
import json
from pprint import pprint, pformat

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
    home = os.getcwd()
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.getcwd()
    print("Performing tests in ", directory)

    current_branch = git_tools.get_current_branch(directory)
    print("\t- Got current GIT branch: {}".format(current_branch))

    history = git_tools.get_git_history(root_directory=directory, branch=current_branch)
    if '--to-file' in sys.argv:
        json.dump(history, open(home+'/git_history.json', 'w'), sort_keys=True, indent=2)
        print("\t- Got GIT history")
        json.dump(git_tools.get_file_history(history), open(home+'/git_file_history.json', 'w'), sort_keys=True, indent=2)
        print("\t- Got GIT file history")
    else:
        pprint(history)
        pprint(git_tools.get_file_history(history))
