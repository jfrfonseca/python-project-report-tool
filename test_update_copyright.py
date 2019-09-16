#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
"""


__copyright__  = 'Copyright (c) 2018 José F. R. Fonseca'
__credits__    = []
__author__     = ''
__maintainer__ = ''
__date__       = '27/09/2018 21:49:38'
__version__    = '0.20180927.3'


"""
# IMPORTS
"""


# Standard Library
import os
import sys
import glob

# Project
from python_project_report_tool import git_tools, update_meta_tags


"""
# RUNTIME
"""


if __name__ == '__main__':
    home = os.getcwd()
    if len(sys.argv) > 2:
        directory_list = sys.argv[1]
        print('Directory List: {}'.format(directory_list))
        if not os.path.exists(directory_list):
            directory_list = glob.glob(directory_list)
            directory_list = [d for d in directory_list if os.path.isdir(d)]
        else:
            directory_list = [directory_list]
        copyright_message = sys.argv[2]
    else:
        directory_list = [os.getcwd()]
        copyright_message = sys.argv[1]

    print('Directories to perform tests on: {}'.format(directory_list))

    for i, directory in enumerate(directory_list):
        print("({}/{}) Performing tests in {}".format(i+1, len(directory_list), directory))
        print("({}/{}) Copyright message: {}".format(i+1, len(directory_list), copyright_message))

        # Get current branch
        current_branch = git_tools.get_current_branch(directory)
        if current_branch == '':
            print("\t- Not a GIT repository (no-branch). Skipping...")
            continue
        print("\t- Got current GIT branch: {}".format(current_branch))

        # Process history
        history = git_tools.get_git_history(root_directory=directory, branch=current_branch)
        print("\t- Got GIT history")
        file_history = git_tools.get_file_history(history)
        print("\t- Got GIT file history")
        for filename, metadata in file_history.items():
            if filename.endswith('.py'):
                path = os.path.join(directory, metadata['file'])
                if metadata['current'] and os.path.isfile(path):
                    updated = update_meta_tags.update_copyright_message(path, copyright_message)
                    if updated:
                        print('\t- Updated {} in {}'.format(filename, path))
