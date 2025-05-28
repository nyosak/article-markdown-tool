#!/usr/bin/env python3

r"""
article publishing tools:
handle git diff; git add -u; for article-qiita-doc.
copyright 2025, hanagai

qiita_diff.py
version: May 28, 2025
"""

import argparse
from conf import *
from common_run import Run
from common_diff import CommonDiff

class QiitaDiff(CommonDiff):
    r"""
    handle git diff; git add -u; for article-qiita-doc.
    """

    dry_run = False

    def git(self):
        r"""
        Git Class to use in this class
        """
        from qiita_git import QiitaGit
        return QiitaGit(skip_initialize=True)

    def local_path(self):
        r"""
        local repo path to use in this class
        """
        return conf_current.QIITA


def main():
  print('main launched manually.')
  description = 'show git diff and do git add -u at qiita-doc.'
  arg_dry = 'disable git add -u (optional)'
  myself = 'qiita_diff.py'

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
  parser.add_argument('-d', '--dry', help=arg_dry, default=False, action='store_true')
  args = parser.parse_args()

  print(args)
  QiitaDiff(dry_run=args.dry).diff_and_add()

if __name__ == '__main__':
    main()
