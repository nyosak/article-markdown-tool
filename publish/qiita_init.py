#!/usr/bin/env python3

r"""
article publishing tools:
create a new article file at qiita-doc.
copyright 2025, hanagai

qiita_init.py
version: May 28, 2025
"""

import re
import datetime
import os.path
from conf import *
from qiita_git import QiitaGit
from qiita_diff import QiitaDiff
from common_run import Run

DRY_RUN = False # disable file writing if True

def new_article(args, git):
    r"""
    create a new article document
    """
    qiita_name = conf_current.qiita_name()
    expected_md = f'{qiita_name}.md'

    command = ['npx', 'qiita', 'new', qiita_name]
    if DRY_RUN:
        created = f'created: {expected_md}'
        print('DRY_RUN: skipping creating new qiita article file')
    else:
        result = Run.run_command(conf_dirs.QIITA, command, return_result=True)
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
        new_file = re.sub(r'^.*: *', '', created)
        # success case will exit the block here.
        if new_file != expected_md:
            print(new_file)
            print(expected_md)
            print(len(new_file))
            print(len(expected_md))
            print(new_file.split())
            message = f'Error: created file {new_file} does not match current name {qiita_name}'
            print(message)
            raise ValueError(message)
    else:
        message = f'Error: {created} {result.stderr.strip()}'
        print(message)
        raise RuntimeError(message)

    print(new_file)
    qiita_path = conf_current.qiita_path()
    print(qiita_path)

    if DRY_RUN:
        print('DRY_RUN: skipping git add')
    else:
        git.git_add(qiita_path)

    return True

def update_from_base(args, git_diff):
    r"""
    update qiita article file from base
    """
    qiita_path = conf_current.qiita_path()
    base_doc = conf_current.a_path()

    print('# BEFORE')
    print_file(qiita_path)

    update_meta(qiita_path, args)

    print('# AFTER META')
    print_file(qiita_path)

    update_doc(qiita_path, base_doc)

    print('# AFTER DOC')
    print_file(qiita_path)

    if DRY_RUN:
        print('DRY_RUN: skipping git add')
    else:
        #git.git_add(qiita_path)
        # no path is needed because it was already added at new
        git_diff.diff_and_add()

def update_meta(qiita_path, args):
    r"""
    update meta information of qiita article
    """
    if DRY_RUN:
        print('DRY_RUN: skipping read initial file')
        initial_content = f"""---
title: {args['key']}
tags:
  - ''
private: false
updated_at: ''
id: null
organization_url_name: null
slide: false
ignorePublish: false
---
# new article body
""".split('\n')
        initial_content.pop() # remove last item that is ''
    else:
        with open(qiita_path, 'r') as file:
            initial_content = file.readlines()
    remove_from_initial = [
        r'^---',
        r'^ +-',
        r'^#',
        r'^title:',
        r'^tags:',
    ]
    remove_pattern = re.compile('|'.join(remove_from_initial))
    cleaned = [item.rstrip() for item in initial_content if not remove_pattern.search(item)]
    print(f'initial: {initial_content}')
    print(f'cleaned: {cleaned}')

    title = args['title']
    tags = '\n'.join(f"  - {tag}" for tag in args['tags'])
    cleaned_string = '\n'.join(cleaned)
    meta = f"""---
title: '{title}'
tags:
{tags}
{cleaned_string}
---
"""
    print(meta)
    if DRY_RUN:
        print(f'DRY_RUN: skipping update meta information')
    else:
        with open(qiita_path, 'w') as qiita_file:
            qiita_file.write(meta)

def update_doc(qiita_path, base_doc):
    r"""
    insert base_doc into qiita article
    """
    if DRY_RUN:
        print(f'DRY_RUN: skipping append {base_doc}')
    else:
        with open(base_doc, 'r') as base_file:
            base_content = base_file.read()
            with open(qiita_path, 'a') as qiita_file:
                qiita_file.write(base_content)

def commit_and_push(git, message):
    r"""
    git commit and push
    """
    qiita_name = conf_current.qiita_name()
    if DRY_RUN:
        print('DRY_RUN: skipping git commit, push')
    else:
        git.git_commit(f'{message}{qiita_name}')
        git.git_push()

def print_file(path):
    r"""
    print file content
    """
    print(f'=== {os.path.relpath(path, conf_current.QIITA)} ===')
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

def make_initial_document_qiita(args):
    r"""
    make initial document for qiita
    """
    notify('Begin')

    git = QiitaGit(skip_initialize=DRY_RUN)
    git_diff = QiitaDiff(dry_run=DRY_RUN)
    new_article(args, git)
    #commit_and_push(git, 'new article: ')
    update_from_base(args, git_diff)
    #commit_and_push(git, 'update from base: ')

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
  make_initial_document_qiita(args)

if __name__ == '__main__':
    main()
