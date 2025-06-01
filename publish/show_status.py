#!/usr/bin/env python3

r"""
article publishing tools:
git status for all
copyright 2025, hanagai

show_status.py
version: June 1, 2025
"""

import argparse
import os.path
from conf import *
from common_run import Run
# it doesn't depend on CommonGit

def git_status_all(target, options):
  for cwd in target:
    print(f'=== {os.path.basename(cwd)} ===')
    command = ['git', 'status']
    command.extend(options)
    Run.run_direct(cwd=cwd, command=command)

def main():
  print('main launched manually.')
  description = "git status for all"
  arg_base = 'only for base (optional)'
  arg_zenn = 'only for zenn (optional)'
  arg_qiita = 'only for qiita (optional)'
  myself = 'show_status.py'

  f"""
  purpose:
    {description}

  usage:
    ./{myself}
    ./{myself} --base
    ./{myself} --zenn
    ./{myself} --qiita
    ./{myself} -s -b (git status options can be used)

  arguments:
    --base: {arg_base}
    --zenn: {arg_zenn}
    --qiita: {arg_qiita}
  """

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('--base', help=arg_base, default=False, action='store_true')
  parser.add_argument('--zenn', help=arg_zenn, default=False, action='store_true')
  parser.add_argument('--qiita', help=arg_qiita, default=False, action='store_true')
  args, options = parser.parse_known_args()

  print(args)

  target = []
  if args.base:
    target.append(conf_current.BASE)
  if args.zenn:
    target.append(conf_current.ZENN)
  if args.qiita:
    target.append(conf_current.QIITA)
  if 0 == len(target):
    target = [conf_current.BASE, conf_current.ZENN, conf_current.QIITA]

  print(target)
  git_status_all(target, options)

if __name__ == '__main__':
    main()
