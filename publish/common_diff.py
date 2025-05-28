#!/usr/bin/env python3

r"""
article publishing tools:
base class to handle git diff; git add -u;
copyright 2025, hanagai

common_diff.py
version: May 28, 2025
"""

import argparse
import datetime
import re
from conf import *
from common_run import Run

class CommonDiff:
    r"""
    base class to handle git diff; git add -u;
    """

    dry_run = False

    def git(self):
        r"""
        Git Class to use in this class
        """
        from common_git import CommonGit
        return CommonGit(skip_initialize=True)

    def local_path(self):
        r"""
        local repo path to use in this class
        """
        return conf_current.BASE

    def __init__(self, dry_run=False):
        # dry_run disables git add -u
        self.dry_run = dry_run

    def __str__(self):
        return (
        f'{self.__class__.__name__}('
        f'{self.local_path()},'
        f')'
        )

    def show_git_diff(self):
        r"""
        show git diff
        """
        command = ['git', 'diff']
        Run.run_direct(self.local_path(), command)

    def show_git_diff_cached(self):
        r"""
        show git diff
        """
        command = ['git', 'diff', '--cached']
        Run.run_direct(self.local_path(), command)

    def show_status(self):
        r"""
        show git status
        """
        command = ['git', 'status', '-s', '-b']
        Run.run_direct(self.local_path(), command)


    def notify(self, message):
        r"""
        notify message
        """
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        doc = re.sub(r'\n', '\n-   ', self.__doc__)
        print(f'''---
    {message} --- {now}
    -   {doc}
    ---
    ''')

    def diff_and_add(self):
        r"""
        make initial documents
        """
        self.notify('Begin')

        self.show_git_diff()
        self.show_git_diff_cached()
        self.show_status()

        if self.dry_run:
            print('DRY RUN: skip git add -u')
            print(self.git())
        else:
            self.git().git_add_u()
            print('files added to staged.')
            self.show_status()

        self.notify('Done')

def main():
  print('main launched manually.')
  description = "DO NOT RUN: it's a base class! show git diff and do git add -u."
  arg_dry = 'disable git add -u (optional)'
  myself = 'common_diff.py'

  f"""
  purpose:
    {description}

  usage:
    ./{myself}
    ./{myself} --dry

  arguments:
    -d: {arg_dry}
  """

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-d', '--dry', help=arg_dry, default=True, action='store_true')
  args = parser.parse_args()

  print(args)
  CommonDiff(dry_run=args.dry).diff_and_add()

if __name__ == '__main__':
    main()
