#!/usr/bin/env python3

r"""
article publishing tools:
help
copyright 2025, hanagai

help.py
version: May 27, 2025
"""

def help_usage():
  help = r'''
# new article

./base_init.py    create a new article document at base-doc.
  -n --name <name>      article short name, REQUIRED, e.g. android_activity
  -s --series <series>  series name, default: a
  -t --title <title>    article title, default: について、とりあえずメモ
  -k --tags <tags>      tags, default: `used tags`
  -z --type <type>      type, default: tech
  -e --emoji <emoji>    emoji, default: 🐚
  -d --date <today>     today as 令和 day, default: today formatted as 70527

./base_diff.py    show git diff, git diff --cached, git status -s -b, git add -u
  -d --dry              disable git add -u

./zenn_init.py    create a new article file at zenn-doc.
./qiita_init.py   create a new article file at qiita-doc.

# publish article

./zenn_previwe.sh   preview zenn article
./qiita_preview.sh  preview qiita article


# edit article published

# edit qiita article only

# edit zenn article only


# miscellaneous

./show_current.py  show current series, type, tags, emoji
./help.py          show this help message
'''
  return help

def main():
  print(help_usage())

if __name__ == '__main__':
  main()
