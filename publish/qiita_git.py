#!/usr/bin/env python3

r"""
article publishing tools:
handle GitHub repository article-qiita-doc.
copyright 2025, hanagai

qiita_git.py
version: May 25, 2025
"""

from common_git import CommonGit
from conf import *

class QiitaGit(CommonGit):
  r"""
  handle GitHub repository article-qiita-doc.
  """

  def local_path(self):
    return conf_dirs.QIITA


# Test function to demonstrate usage
def test():
  print('test launched manually.')
  b = QiitaGit(skip_initialize=True)
  print(b)

if __name__ == '__main__':
  test()
