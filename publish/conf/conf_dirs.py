#!/usr/bin/env python3

r"""
article publishing tools:
module conf:
local directories
copyright 2025, hanagai

conf/conf_dirs.py
version: May 22, 2025
"""

import os.path

HOME = os.path.expanduser('~')
# absolute path configuration
#DOC_HOME = f'{HOME}/doc'
# relative path configuration
# expects to be run from article-markdown-tool/publish directory
#DOC_HOME = os.path.abspath('../..')
# relative to this file
DOC_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

BASE = os.path.join(DOC_HOME, 'article-base-doc')
QIITA = os.path.join(DOC_HOME, 'article-qiita-doc')
ZENN = os.path.join(DOC_HOME, 'article-zenn-doc')
TOOL = os.path.join(DOC_HOME, 'article-markdown-tool')
TMP = os.path.join(TOOL, 'tmp')

def test():
  print('test launched manually.')
  print('HOME:', HOME)
  print('DOC_HOME:', DOC_HOME)
  print('BASE:', BASE)
  print('QIITA:', QIITA)
  print('ZENN:', ZENN)
  print('TOOL:', TOOL)
  print('TMP:', TMP)
  print(os.path.abspath(__file__))
  print(os.path.abspath('.'))

if __name__ == '__main__':
    test()
