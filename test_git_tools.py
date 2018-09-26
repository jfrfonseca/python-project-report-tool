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
from pprint import pprint

# Project
from python_project_report_tool import git_tools
from python_project_report_tool import versioning_schema


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

    # Get current branch
    current_branch = git_tools.get_current_branch(directory)
    print("\t- Got current GIT branch: {}".format(current_branch))

    # Process history
    history = git_tools.get_git_history(root_directory=directory, branch=current_branch)
    print("\t- Got GIT history")
    file_history = git_tools.get_file_history(history)
    print("\t- Got GIT file history")
    history_pairs = list(file_history.items())
    versions_list = versioning_schema.constant__day__commit_count([record for file_name, record in history_pairs], '0')
    for version, history_pair in zip(versions_list, history_pairs):
        file_name, record = history_pair
        file_history[file_name]['version'] = version
    print("\t- Generated version numbers")

    # Test if printing to file
    to_print = True
    if '--to-file' in sys.argv:
        print("Writing JSON files")
        json.dump(history, open(os.path.join(directory, 'git_history.json'), 'w'), sort_keys=True, indent=2)
        json.dump(file_history, open(os.path.join(directory, 'git_file_history.json'), 'w'), sort_keys=True, indent=2)
        to_print = False

    if '--to-excel' in sys.argv:
        print("Writing MS EXCEL files")
        import pandas as pd
        pd.DataFrame(history).to_excel(os.path.join(directory, 'git_history.xlsx'))
        pd.DataFrame(file_history).T[[
            'current', 'filename',
            'last_update', 'version', 'commits',
            'creation', 'maintainer', 'author', 'credits',
            'path', 'file'
        ]].sort_values(['current', 'path', 'filename']
        ).to_excel(os.path.join(directory, 'git_file_history.xlsx'), index=None, encoding='latin-1')
        to_print = False

    if '--to-csv' in sys.argv:
        print("Writing CSV files")
        import pandas as pd
        pd.DataFrame(history).to_csv(os.path.join(directory, 'git_history.csv'), sep='\t')
        pd.DataFrame(file_history).T.reset_index(drop=True).to_csv(os.path.join(directory, 'git_file_history.csv'), sep='\t')
        to_print = False

    # Test if printing to stdout
    if to_print:
        pprint(history)
        pprint(file_history)
