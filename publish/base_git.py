#!/usr/bin/env python3

r"""
article publishing tools:
handle GitHub repository article-base-doc.
copyright 2025, hanagai

base_git.py
version: June 1, 2025
"""

from common_git import CommonGit
from conf import *

class BaseGit(CommonGit):
  r"""
  handle GitHub repository article-base-doc.
  """

  def local_path(self):
    return conf_dirs.BASE


# Test function to demonstrate usage
def test():
  print('test launched manually.')
  b = BaseGit(skip_initialize=True)
  print(b)
  #print(b.is_danger_here())
  #print(b.git_add('test'))

if __name__ == '__main__':
  test()
