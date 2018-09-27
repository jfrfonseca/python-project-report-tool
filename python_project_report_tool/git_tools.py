#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
"""


__copyright__  = 'Copyright (c) 2018 José F. R. Fonseca'
__credits__    = []
__author__     = ''
__maintainer__ = ''
__date__       = '27/09/2018 21:24:04'
__version__    = '0.20180927.7'


"""
# IMPORTS
"""


# Standard Library
import os
import datetime
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


git_datetime_format = '%a %b %d %H:%M:%S %Y %z'


"""
# UTIL
"""


def parse_git_date(git_date):
    return datetime.datetime.strptime(git_date, git_datetime_format)


def get_current_branch(root_directory=None):
    if root_directory is None:
        root_directory = os.getcwd()
    os.chdir(root_directory)

    # We use GIT's function to retrieve the current branch name
    p = subprocess.Popen(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    try:
        branch = out.decode('string-escape').strip()
    except:
        branch = out.decode('utf-8').strip()

    return branch


def get_git_history(root_directory=None, branch=None):
    if root_directory is None:
        root_directory = os.getcwd()
    os.chdir(root_directory)

    # We retrieve the current branch for default
    if branch is None:
        branch = get_current_branch(root_directory)

    # Run the git command to get commits per filename in a subprocess and get the results, decoded
    process = subprocess.Popen(['git', 'log', branch, '--follow', '--name-only', '.'], stdout=subprocess.PIPE)
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
                    'filename': file.split(os.sep)[-1],
                    'path': os.sep.join(file.split(os.sep)[:-1]),
                    'credits': [commit['author']],
                    'author': commit['author'],
                    'maintainer': commit['author'],
                    'last_update': commit['date'],
                    'creation': commit['date'],
                    'commits': 1,
                    'current': (os.path.exists(file) == 1)
                }

    return history_per_file
