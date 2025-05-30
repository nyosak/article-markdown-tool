#!/usr/bin/env python3

r"""
article publishing tools:
git commit; push; for article-base-doc.
copyright 2025, hanagai

base_commit.py
version: May 30, 2025
"""

import argparse
from conf import *
from base_git import BaseGit

def commit_and_push(message):
  r"""
  git commit and push
  """
  article_name = conf_current.get_current('key')
  git = BaseGit(skip_initialize=True)
  #print(git)
  #print(message)
  #print(article_name)
  git.git_commit(f'{message} {article_name}')
  git.git_push()


def main():
  print('main launched manually.')
  description = 'git commit; push; for article-base-doc.'
  arg_message = 'commit message (optional)'
  myself = 'base_commit.py'
  default_message = 'update'

  f"""
  purpose:
    {description}

  usage:
    ./{myself}
    ./{myself} -m 'ultra super ultimate important commit!!!'

  arguments:
    -m: {arg_message}
  """

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-m', '--message', help=arg_message, default=default_message)
  args = parser.parse_args()

  print(args)
  commit_and_push(args.message)

if __name__ == '__main__':
  main()
