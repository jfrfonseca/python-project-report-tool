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
from collections import Counter


"""
# CONFIG
"""


"""
# UTIL
"""


def count_commits_per_file(root_directory=None):
    if root_directory is None:
        root_directory = os.getcwd()

    # Run the git command to count commits per filename in a subprocess and get the results
    process = subprocess.Popen(['git', 'log', '--follow', '--name-only', root_directory], stdout=subprocess.PIPE)
    out, err = process.communicate()

    # Decodificamos a resposta
    try:
        out = out.decode('string-escape')
    except:
        out = out.decode('utf-8')

    from pprint import pprint
    pprint(out)

    # Return a dictionary with the count of commits per file
    return dict(Counter([line.strip() for line in out.splitlines()]))

