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
import os
import sys
import glob
import datetime

# Project
from python_project_report_tool import git_tools, update_meta_tags
from python_project_report_tool.versioning_schema.constant__day__commit_count import __format_record__constant__day__commit_count


"""
# RUNTIME
"""


if __name__ == '__main__':
    home = os.getcwd()
    if len(sys.argv) > 2:
        directory_list = sys.argv[1]
        if not os.path.exists(directory_list):
            directory_list = glob.glob(directory_list)
            directory_list = [d for d in directory_list if os.path.isdir(d)]
        else:
            directory_list = [directory_list]
        major_version = sys.argv[2]
    else:
        directory_list = [os.getcwd()]
        major_version = sys.argv[1]

    print("Major version: {}".format(major_version))
    print('Directories to perform tests on: {}'.format(directory_list))

    for directory in directory_list:
        print("Performing tests in ", directory)

        # Get current branch
        current_branch = git_tools.get_current_branch(directory)
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

                    date = git_tools.parse_git_date(metadata['last_update'])
                    if date.date() != datetime.date.today():

                        date = date.strftime("%d/%m/%Y %H:%M:%S")
                        updated = update_meta_tags.update_date(path, date)
                        if updated:
                            print('Updated date {} in {}'.format(filename, path))

                        version = __format_record__constant__day__commit_count(metadata, major_version)
                        updated = update_meta_tags.update_version(path, version)
                        if updated:
                            print('Updated version {} in {}'.format(filename, path))
