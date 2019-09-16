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
    ignore_regex = None
    if len(sys.argv) > 1:
        directory_list = sys.argv[1]
        if not os.path.exists(directory_list):
            directory_list = glob.glob(directory_list)
            directory_list = [d for d in directory_list if os.path.isdir(d)]
        else:
            directory_list = [directory_list]
        if len(sys.argv) > 2:
            ignore_regex = sys.argv[2]
    else:
        directory_list = [os.getcwd()]

    simulate = '--simulate' in sys.argv
    print('Directories to perform tests on: {}{}'.format(directory_list, ' - SIMULATE' if simulate else ''))

    if ignore_regex is not None:
        ignore_regex = re.compile(ignore_regex)
        print('File name RegEx to ignore: {}'.format(ignore_regex))

    for i, directory in enumerate(directory_list):
        print("({}/{}) Performing tests in {}".format(i+1, len(directory_list), directory))

        # Files in directory:
        files_in_directory = os.listdir(directory)
        print(files_in_directory)

        # Get local major version
        major_version = 0
        for file_name in ['README.MD', 'README.md', 'readme.MD', 'readme.md',
                          'README.TXT', 'README.txt', 'readme.TXT', 'readme.txt']:
            if file_name in files_in_directory:
                with open(os.path.join(directory, file_name), 'r') as fin:
                    file_data = fin.read()
                search_results = re.search('VERSION:\s*(\d+)', file_data)
                if search_results is None:
                    continue
                major_version = int(search_results.group(1))
                print('\t- Got {} version: {}'.format(file_name, major_version))
                break

        print("\t- Got Major Version: {}".format(major_version))

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
                if (ignore_regex is not None) and (ignore_regex.match(filename)):
                    continue
                path = os.path.join(directory, metadata['file'])
                if metadata['current'] and os.path.isfile(path):

                    date = git_tools.parse_git_date(metadata['last_update'])
                    if date.date() != datetime.date.today():

                        date = date.strftime("%d/%m/%Y %H:%M:%S")
                        updated = update_meta_tags.update_date(path, date, simulate=simulate)
                        if updated:
                            print('\t- Updated date {} in {}{}'.format(filename, path, ' - SIMULATE' if simulate else ''))

                        version = __format_record__constant__day__commit_count(metadata, major_version)
                        updated = update_meta_tags.update_version(path, version, simulate=simulate)
                        if updated:
                            print('\t- Updated version {} in {}{}'.format(filename, path, ' - SIMULATE' if simulate else ''))
