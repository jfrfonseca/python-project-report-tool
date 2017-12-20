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
import subprocess

# PIP
import parse


"""
# CONFIG
"""


commit_report_pattern = parse.compile('''commit {:x}
Author: {}
Date:   {}

{}

{}

''')


"""
# UTIL
"""


def get_git_history(root_directory=None):
    if root_directory is None:
        root_directory = os.getcwd()

    # Run the git command to get commits per filename in a subprocess and get the results, decoded
    process = subprocess.Popen(['git', 'log', '--follow', '--name-only', root_directory], stdout=subprocess.PIPE)
    out, err = process.communicate()
    try:
        out = out.decode('string-escape')
    except:
        out = out.decode('utf-8')

    # Parse the resulting commit metadata
    history = []
    for commit in commit_report_pattern.findall(out+'\n'):
        history.append({
            "commit": str(hex(commit[0])),
            "author": commit[1],
            "date": commit[2],
            "message": commit[3],
            "files": commit[4].splitlines()
        })

    # Return in reverse order (chronological order
    history.reverse()
    return history


def get_file_history(git_history):
    history_per_file = {}

    # For each commit in the history
    for commit in git_history:

        # For each file in the current commit
        for file in commit['files']:

            # Insert or update the file's metadata
            if file in history_per_file:
                history_per_file[file].update({
                    'credits': sorted(list(set(history_per_file[file]['credits'] + [commit['author']]))),
                    'maintainer': commit['author'],
                    'last_update': commit['date'],
                    'commits': history_per_file[file]['commits'] + 1,
                })
            else:
                history_per_file[file] = {
                    'file': file,
                    'credits': [commit['author']],
                    'author': commit['author'],
                    'maintainer': commit['author'],
                    'last_update': commit['date'],
                    'creation': commit['date'],
                    'commits': 1,
                }

    return history_per_file
