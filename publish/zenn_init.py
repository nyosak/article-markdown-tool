#!/usr/bin/env python3

r"""
article publishing tools:
create a new article file at zen-doc.
copyright 2025, hanagai

zen_init.py
version: May 28, 2025
"""

import re
import datetime
import os.path
from conf import *
from zenn_git import ZennGit
from zenn_diff import ZennDiff
from common_run import Run

DRY_RUN = False # disable file writing if True

def new_article(git):
    r"""
    create a new article document
    """
    zenn_name = conf_current.zenn_name()
    expected_md = f'{zenn_name}.md'

    command = ['npx', 'zenn', 'new:article', '--slug', zenn_name]
    if DRY_RUN:
        created = f'created: articles/{expected_md}'
        print('DRY_RUN: skipping creating new zenn article file')
    else:
        result = Run.run_command(conf_dirs.ZENN, command, return_result=True)
        lines = result.stdout.strip().split('\n')
        created_line = [line for line in lines if re.search(r'^created:', line)]
        # lines may contain other information (e.g. update to new version, pls.)
        if len(created_line) == 1:
            created = re.sub(r'\x1b\[\w*?$', '', created_line[0].strip(), count=1)
            # screen output may contain esc seq to control colors and so on.
            # remove the last seq (back to normal) only here by minimum match.
        else:
            message = f'Error: something wrong for new:article output.\n{lines}'
            print(message)
            raise ValueError(message)

    if re.search(r'^created:', created):
        print(f'created: {created}')
        new_file = re.sub(r'^.*/', '', created)
        # success case will exit the block here.
        if new_file != expected_md:
            print(new_file)
            print(expected_md)
            print(len(new_file))
            print(len(expected_md))
            print(new_file.split())
            message = f'Error: created file {new_file} does not match current name {zenn_name}'
            print(message)
            raise ValueError(message)
    else:
        message = f'Error: {created} {result.stderr.strip()}'
        print(message)
        raise RuntimeError(message)

    print(new_file)
    # this should be after the file creation, to avoid creating another name
    zenn_path = conf_current.zenn_path()
    print(zenn_path)

    if DRY_RUN:
        print('DRY_RUN: skipping git add')
    else:
        git.git_add(zenn_path)

    return True

def update_from_base(args, git_diff):
    r"""
    update zenn article file from base
    """
    zenn_path = conf_current.zenn_path()
    base_doc = conf_current.a_path()

    print('# BEFORE')
    print_file(zenn_path)

    update_meta(zenn_path, args)

    print('# AFTER META')
    print_file(zenn_path)

    update_doc(zenn_path, base_doc)

    print('# AFTER DOC')
    print_file(zenn_path)

    if DRY_RUN:
        print('DRY_RUN: skipping git add')
    else:
        #git.git_add(zenn_path)
        # no path is needed because it was already added at new
        git_diff.diff_and_add()

def update_meta(zenn_path, args):
    r"""
    update meta information of zenn article
    """
    title = args['title']
    tech = args['type']
    emoji = args['emoji']
    topics = '["' + '", "'.join(args['tags']) + '"]'
    meta = f'''---
title: "{title}"
topics: {topics}
type: "{tech}"
emoji: "{emoji}"
published: true
---
'''
    print(meta)
    if DRY_RUN:
        print(f'DRY_RUN: skipping update meta information')
    else:
        with open(zenn_path, 'w') as zenn_file:
            zenn_file.write(meta)

def update_doc(zenn_path, base_doc):
    r"""
    insert base_doc into zenn article
    """
    if DRY_RUN:
        print(f'DRY_RUN: skipping append {base_doc}')
    else:
        with open(base_doc, 'r') as base_file:
            base_content = base_file.read()
            with open(zenn_path, 'a') as zenn_file:
                zenn_file.write(base_content)

def commit_and_push(git, message):
    r"""
    git commit and push
    """
    zenn_name = conf_current.zenn_name()
    if DRY_RUN:
        print('DRY_RUN: skipping git commit, push')
    else:
        git.git_commit(f'{message}{zenn_name}')
        git.git_push()

def print_file(path):
    r"""
    print file content
    """
    print(f'=== {os.path.relpath(path, conf_current.ZENN)} ===')
    if DRY_RUN:
        print('DRY_RUN: skipping print file')
    else:
        with open(path, 'r') as file:
            content = file.read()
            print(content)
    print("======")

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

def make_initial_document_zenn(args):
    r"""
    make initial document for zenn
    """
    notify('Begin')

    git = ZennGit(skip_initialize=DRY_RUN)
    git_diff = ZennDiff(dry_run=DRY_RUN)
    new_article(git)
    commit_and_push(git, 'new article: ')
    update_from_base(args, git_diff)
    commit_and_push(git, 'update from base: ')

    notify('Done')

def get_current():
    r"""
    get current configuration
    """
    yaml = conf_current.read_yaml(conf_current.meta_path())
    keys = ['key', 'name', 'now']
    for key in keys:
        yaml[key] = conf_current.get_current(key)
    return yaml

def main():
  print('main launched manually.')
  args = get_current()
  print(args)
  make_initial_document_zenn(args)

if __name__ == '__main__':
    main()
