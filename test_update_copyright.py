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

# Project
from python_project_report_tool import git_tools, update_copyright


"""
# RUNTIME
"""


if __name__ == '__main__':
    home = os.getcwd()
    if len(sys.argv) > 2:
        directory = sys.argv[1]
        copyright_message = sys.argv[2]
    else:
        directory = os.getcwd()
        copyright_message = sys.argv[1]
    print("Performing tests in ", directory)
    print("Copyright message: {}".format(copyright_message))

    # Get current branch
    current_branch = git_tools.get_current_branch(directory)
    print("\t- Got current GIT branch: {}".format(current_branch))

    # Process history
    history = git_tools.get_git_history(root_directory=directory, branch=current_branch)
    print("\t- Got GIT history")
    file_history = git_tools.get_file_history(history)
    print("\t- Got GIT file history")
    for file in file_history:
        if file['current']:
            if file['filename'].endswith('.py'):
                update_copyright.update_copyright_message(file['path'], copyright_message)
