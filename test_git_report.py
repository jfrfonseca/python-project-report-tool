#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
"""


__copyright__  = 'Copyright (c) 2018 José F. R. Fonseca'
__credits__    = []
__author__     = ''
__maintainer__ = ''
__date__       = '27/09/2018 21:24:04'
__version__    = '0.20180927.9'


"""
# IMPORTS
"""


# Standard Library
import re
import os
import sys
import glob
from datetime import date

# PIP
import pandas as pd

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

    if ignore_regex is not None:
        ignore_regex = re.compile(ignore_regex)
        print('File name RegEx to ignore: {}'.format(ignore_regex))

    data = None
    for i, directory in enumerate(directory_list):
        print("({}/{}) Acquiring data in {}".format(i+1, len(directory_list), directory))

        # Files in directory:
        files_in_directory = os.listdir(directory)

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
        history = pd.DataFrame(git_tools.get_git_history(root_directory=directory, branch=current_branch))
        history.loc[:, 'major_version'] = major_version
        history.loc[:, 'branch'] = current_branch
        history.loc[:, 'project'] = (directory[:-1] if directory.endswith('/') else directory).split('/')[-1]
        print("\t- Got GIT history")
        if data is None:
            data = history
        else:
            data = data.append(history)

    # Dump the data
    file = date.today().strftime(os.path.join(home, 'git_history_%Y-%m-%d.xlsx'))
    data.loc[:, 'number_of_files'] = data['files'].apply(lambda i: len(i))
    data.loc[:, 'date_1'] = pd.to_datetime(
        data['date'].astype(str).apply(lambda d: d.split('+')[0].split('-')[0].strip()),
        format='%a %b %d %H:%M:%S %Y'
    )
    data.loc[:, 'tz'] = data['date'].astype(str).apply(
        lambda d: d.split('2015')[-1].split('2016')[-1].split('2017')[-1].split('2018')[-1].split('2019')[-1].strip().replace(' ', '')
    ).astype(int)
    data.loc[:, 'date'] = pd.to_datetime((data['date_1'].astype(int) + (3600000000000 * data['tz'])), unit='ns').dt.strftime('%Y-%m-%d %H:%M:%S')
    data = data[~data['project'].isin(['python-project-report-tool'])]
    data[
        ['project', 'major_version', 'branch', 'date', 'author', 'commit', 'message', 'number_of_files']
    ].sort_values(['project', 'date', 'commit']).to_excel(file, index=None)
    print('Data dumped to file {}'.format(file))

    sys.exit(0)
