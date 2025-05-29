#!/usr/bin/env python3

r"""
article publishing tools:
create and update an article file for zenn.
copyright 2025, hanagai

zenn_init.py
version: May 29, 2025
"""

import argparse
from conf import *
from common_run import Run
from zenn_update import ZennUpdate


def main():
  print('main launched manually.')
  description = 'create an article file for zenn.'
  arg_dry = 'disable file writing and git (optional)'
  arg_nogit = 'disable git (optional)'
  myself = 'zenn_init.py'

  f"""
  purpose:
    {description}

  usage:
    ./{myself}
    ./{myself} --dry
    ./{myself} --nogit

  arguments:
    -d: {arg_dry}
    -n: {arg_nogit}
  """

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-d', '--dry', help=arg_dry, default=False, action='store_true')
  parser.add_argument('-n', '--nogit', help=arg_nogit, default=False, action='store_true')
  args = parser.parse_args()

  print(args)
  ZennUpdate(dry_run=args.dry,no_git=args.nogit).make_initial()

if __name__ == '__main__':
    main()
