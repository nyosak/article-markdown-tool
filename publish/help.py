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
./base_add_media.py   TODO copy and git add pictures
./base_commit.py      git commit, push
  -m --message          commit message, default: update

./zenn_init.py    create a new article file at zenn-doc.
  -d --dry              disable file writing and git
  -n --nogit            disable git
./qiita_init.py   create a new article file at qiita-doc.
  -d --dry              disable file writing and git
  -n --nogit            disable git

./zenn_update.py  update current new article file at zenn-doc.
  -d --dry              disable file writing and git
  -n --nogit            disable git
./qiita_update.py update current new article file at qiita-doc.
  -d --dry              disable file writing and git
  -n --nogit            disable git

# publish article

./zenn_previwe.sh   preview zenn article
./qiita_preview.sh  preview qiita article

./all_publish.py    base_publish, zenn_publish and qiita_publish
  -d --dry              disable git writing
  -n --nomerge          create pull request, but not merge it
  -i --ignore           ignore uncommitted changes

# edit article published

./base_checkout.py  TODO

# edit qiita article only

./qiita_checkout.py TODO

# edit zenn article only

./zenn_checkout.py  TODO

# miscellaneous

./show_current.py  show current series, name, key, now
./help.py          show this help message
'''
  return help

def main():
  print(help_usage())

if __name__ == '__main__':
  main()
