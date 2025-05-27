#!/usr/bin/env python3

r"""
article publishing tools:
git diff; git add -u;s at base-doc.
copyright 2025, hanagai

base_diff.py
version: May 27, 2025
"""

import argparse
import datetime
import re
from conf import *
from base_git import BaseGit
from common_run import Run

def show_git_diff():
    r"""
    show git diff
    """
    command = ['git', 'diff']
    Run.run_direct(conf_current.BASE, command)

def show_git_diff_cached():
    r"""
    show git diff
    """
    command = ['git', 'diff', '--cached']
    Run.run_direct(conf_current.BASE, command)

def show_status():
    r"""
    show git status
    """
    command = ['git', 'status', '-s', '-b']
    Run.run_direct(conf_current.BASE, command)

def git_add_u(args, git):
    r"""
    git add -u
    """

def notify(message):
    r"""
    notify message
    """
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    doc = re.sub(r'\n', '\n-   ', __doc__)
    print(f'''---
{message} --- {now}
-   {doc}
---
''')

def diff_and_add(args):
    r"""
    make initial documents
    """
    notify('Begin')

    git = BaseGit(skip_initialize=True)
    show_git_diff()
    show_git_diff_cached()
    show_status()

    if args['dry']:
        print('DRY RUN: skip git add -u')
    else:
        git.git_add_u()
        print('files added to staged.')
        show_status()

    notify('Done')

def main():
  print('main launched manually.')
  description = 'show git diff and do git add -u at base-doc.'
  arg_dry = 'disable git add -u (optional)'

  f"""
  purpose:
    {description}

  usage:
    ./base_diff.py
    ./base_diff.py --dry

  arguments:
    -d: {arg_dry}
  """

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-d', '--dry', help=arg_dry, default=False, action='store_true')
  args = parser.parse_args()

  print(args)
  diff_and_add(args.__dict__)

if __name__ == '__main__':
    main()
