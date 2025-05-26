#!/usr/bin/env python3

r"""
article publishing tools:
create a new document files at base-doc.
copyright 2025, hanagai

base_init.py
version: May 27, 2025
"""

import argparse
import os
import datetime
import re
from conf import *
from base_git import BaseGit

DRY_RUN = False # disable file writing yaml and md if True

DEFAULT_SERIES = 'a'
DEFAULT_TITLE = 'について、とりあえずメモ'
DEFAULT_TAGS = 'Android Activity Fragment RecyclerView GitHub Token Ubuntu'
DEFAULT_TYPE = 'tech'
DEFAULT_EMOJI = '🐚'
MAX_USED_TAGS = 0 # positive: used top, zero: used all, negative: default
YAML_KEYS = ('title', 'tags', 'type', 'emoji')

def initial_yaml(args):
    r"""
    initial yaml file
    """
    lines = [f'{key}: {args[key]}' for key in YAML_KEYS]
    return '\n'.join(lines + [''])

def initial_md(args):
    r"""
    initial md document template
    """
    template = '''# %s

---

# 🌒️ 序

# 🌕️ 破

# 🌖️ 急

'''
    return template % args['title']

def get_current_series():
    r"""
    get current series
    """
    series = conf_current.get_current('series')
    return DEFAULT_SERIES if series is None else series

def set_current(args):
    r"""
    set current series, name
    """
    conf_current.set_current('now', args['date'])
    conf_current.set_current('series', args['series'])
    conf_current.set_current('name', args['name'])
    conf_current.set_current('key', f"{args['date']}_{args['name']}")

def write_yaml(args, git):
    r"""
    write yaml file and git add
    """
    path = conf_current.meta_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    yaml = initial_yaml(args)
    print(f'\nyaml path: {path}')
    print(yaml)
    if DRY_RUN:
        print('DRY RUN: skip writing yaml file')
    else:
        with open(path, 'w') as f:
            f.write(yaml)
        git.git_add(path)

def write_md(args, git):
    r"""
    write md file and git add
    """
    path = conf_current.a_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    md = initial_md(args)
    print(f'\nmd path: {path}')
    print(md)
    if DRY_RUN:
        print('DRY RUN: skip writing md file')
    else:
        with open(path, 'w') as f:
            f.write(md)
        git.git_add(path)

def modify_readme(args, git):
    r"""
    modify README.md file and git add
    """
    path = conf_current.readme_path()
    print(f'\nreadme path: {path}')
    if path is None:
        print('readme path is None, skip modifying README.md')
        return

    with open(path, 'r') as f:
        lines = f.readlines()

    key = '<!-- ARTICLES DESCENDANT -->\n'
    if not key in lines:
        print(f'readme file does not contain {repr(key)}, skip modifying README.md')
        return
    insert_after = lines.index(key)
    print(f'insert after: {insert_after} line')
    link = f'- [{args["title"]}]({os.path.relpath(conf_current.a_path(), conf_current.BASE)})\n'
    print(f'link: {link}')
    lines.insert(insert_after + 1, link)
    #print(lines)

    if DRY_RUN:
        print('DRY RUN: skip writing readme file')
    else:
        with open(path, 'w') as f:
            f.writelines(lines)
        git.git_add(path)

def commit_and_push(git):
    r"""
    commit and push
    """
    if DRY_RUN:
        print('DRY RUN: skip git commit and push')
    else:
        git.git_commit(f'initialize {conf_current.get_current("name")}')
        git.git_push()

def notify(message):
    r"""
    notify message
    """
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    doc = re.sub(r'\n', '\n-   ', __doc__)
    print(f'''---
{message} --- {now}
-   {doc}
---
''')

def make_initial_documents(args):
    r"""
    make initial documents
    """
    notify('Begin')

    set_current(args)
    git = BaseGit(skip_initialize=DRY_RUN)
    write_yaml(args, git)
    write_md(args, git)
    modify_readme(args, git)
    commit_and_push(git)

    notify('Done')

def main():
  print('main launched manually.')
  description = 'create a new document files at base-doc.'
  arg_s = 'series (parent folder)'
  arg_n = 'core file name of this article (use [0-9a-z_])'
  arg_title = 'title of this article (optional)'
  arg_tags = 'tags of this article (optional)'
  arg_type = 'type of this article (optional)'
  arg_emoji = 'emoji of this article (optional)'
  arg_date = 'date of this article (optional)'

  f"""
  purpose:
    {description}

  usage:
    ./base_init.py -s a -n recycler_view
    ./base_init.py -n recycler_view

  arguments:
    -s: {arg_s}
    -n: {arg_n}
    -t: {arg_title}
    -k: {arg_tags}
    -z: {arg_type}
    -e: {arg_emoji}
    -d: {arg_date}
  """

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-s', '--series', help=arg_s, default=get_current_series())
  parser.add_argument('-n', '--name', help=arg_n, required=True)
  parser.add_argument('-t', '--title', help=arg_title, default=DEFAULT_TITLE)
  parser.add_argument('-k', '--tags', help=arg_tags, default=DEFAULT_TAGS if MAX_USED_TAGS < 0 else conf_current.used_tags_str(MAX_USED_TAGS))
  parser.add_argument('-z', '--type', help=arg_type, default=DEFAULT_TYPE)
  parser.add_argument('-e', '--emoji', help=arg_emoji, default=DEFAULT_EMOJI)
  parser.add_argument('-d', '--date', help=arg_date, default=conf_current.reiwa_now())
  args = parser.parse_args()

  print(args)
  make_initial_documents(args.__dict__)

if __name__ == '__main__':
    main()
