#!/usr/bin/env python3

r"""
article publishing tools:
help
copyright 2025, hanagai

help.py
version: June 8, 2025
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
./base_add_media.py   copy and git add pictures
  -f --files            source files to copy into base media
  -d --dry              disable file writing and git
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

./nolook_publish.py zenn_init/update, qiita init/update and all_publish
  --publish             required to confirm
  -d --dry              disable git writing
  -n --nomerge          create pull request, but not merge it
  -i --ignore           ignore uncommitted changes

# edit article published

./base_checkout.py  checkout article published for base.
  1st                   key to checkout; 70530_publish_zenn_qiita
  -d --dry              disable changes

# edit qiita article only

./qiita_checkout.py checkout article published for zenn.
  1st                   key to checkout; 70530_publish_zenn_qiita
  -d --dry              disable changes

# edit zenn article only

./zenn_checkout.py  checkout article published for qiita.
  1st                   key to checkout; 70530_publish_zenn_qiita
  -d --dry              disable changes

# miscellaneous

./show_current.py  show current series, name, key, now
./show_status.py   git status for all repositories
./base_ls.sh       list files at base
  1st              key to list (partial is acceptable)
./base_editor.sh   open editor to edit files at base
  1st              key to edit (partial is acceptable)
                   `current` to edit file for current branch
  2nd              `yaml` to edit yaml files rather than md (optional)
  3rd              editor command (optional)
./help.py          show this help message
'''
  return help

def main():
  print(help_usage())

if __name__ == '__main__':
  main()
