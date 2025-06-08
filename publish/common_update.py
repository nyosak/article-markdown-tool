#!/usr/bin/env python3

r"""
article publishing tools:
base class to create and update an article file from base.
copyright 2025, hanagai

common_update.py
version: June 8, 2025
"""

import re
import datetime
import os.path
from conf import *
from common_run import Run

class CommonUpdate:
    r"""
    base class to create and update an article file from base.
    """

    dry_run = False
    no_git = False
    pager = True
    current = {}
    _git = None
    _git_diff = None

    def git(self):
        r"""
        Git Class to use in this class
        """
        if self._git is None:
            print('initialize _git')
            from common_git import CommonGit
            self._git = CommonGit(skip_initialize=self.dry_run)
        return self._git

    def git_diff(self):
        r"""
        Git Diff Class to use in this class
        """
        if self._git_diff is None:
            print('initialize _git_diff')
            from common_diff import CommonDiff
            self._git_diff = CommonDiff(dry_run=self.dry_run)
        return self._git_diff

    def local_path(self):
        r"""
        local repo path to use in this class
        """
        return conf_dirs.BASE

    def article_name(self):
        r"""
        article name of target
        """
        #return conf_current.zenn_name()
        #return conf_current.qiita_name()
        return conf_current.get_current('key')

    def article_path(self):
        r"""
        article path of target
        """
        #return conf_current.zenn_path()
        #return conf_current.qiita_path()
        return conf_current.a_path()

    def command_new(self, article):
        r"""
        command to generate a new article
        """
        #return ['npx', 'zenn', 'new:article', '--slug', article]
        #return ['npx', 'qiita', 'new', article]
        return ['echo', 'npx', 'zenn/qiita', 'new_something', article]

    def create_meta_head(article_pathself, article_path=None):
        r"""
        create meta information string of current article
        """
        title = self.current['title']
        tech = self.current['type']
        emoji = self.current['emoji']
        topics = '["' + '", "'.join(self.current['tags']) + '"]'
        meta = f'''---
title: "{title}"
topics: {topics}
type: "{tech}"
emoji: "{emoji}"
published: true
---
'''
        print(meta)
        return meta

    def example_stdout_at_new(self, expected_md):
        r"""
        mock output to use for dry_run
        """
        esc_in = '\x1b[32m'
        esc_out = '\x1b[39m'
        #extra_info = ''
        extra_info = f'''

   ╭───────────────────────────────────────────────────────────────╮
   │                                                               │
   │   新しいバージョンがリリースされています: 0.1.160 → {esc_in}0.1.161{esc_out}   │
   │   npm install zenn-cli@latest で更新してください              │
   │                                                               │
   ╰───────────────────────────────────────────────────────────────╯

error: slugの値（hoge）が不正です。小文字の半角英数字（a-z0-9）、ハイフン（-）、アンダースコア（_）の12〜50字の組み合わせにしてください

'''
        out = f'''{extra_info}
created: {esc_in}articles/{expected_md}{esc_out}
'''
        #out = 'created: hoge.md'
        #out = "Error: 'hoge.md' is already exist"
        return out

    def transform_doc_md(self, content):
        r"""
        transform md
        """
        return content


    r"""
    override methods before this line in the class
    """

    @classmethod
    def get_current(cls):
        r"""
        get current configuration
        """
        yaml = conf_current.read_yaml(conf_current.meta_path())
        keys = ['key', 'name', 'now']
        for key in keys:
            yaml[key] = conf_current.get_current(key)
        return yaml

    def __init__(self, dry_run=False, no_git=False, pager=True):
        # dry_run disables file writing and git
        # no_git disables git only
        # pager disables git diff pager when False
        self.dry_run = dry_run
        self.no_git = no_git
        self.pager = pager
        self.current = self.get_current()

    def __str__(self):
        return (
        f'{self.__class__.__name__}('
        f'{self.local_path()},'
        f')'
        )

    def extract_name_created(self, out):
        r"""
        extract and return md file name of creation from stdout string
        """
        lines = out.split('\n')
        created_line = [line for line in lines if re.search(r'^created:', line)]
        # lines may contain other information (e.g. update to new version, pls.)
        if len(created_line) == 1:
            without_key = re.sub(r'^created: *', '', created_line[0].strip())
            print(without_key)
            without_esc = re.sub(r'\x1b\[[^m]*m', '', without_key)
            without_dir = re.sub(r'.*/', '', without_esc)
            # screen output may contain esc seq to control colors and so on.
            # remove the last seq (back to normal) only here by minimum match.
        else:
            message = f'Error: something wrong for new article output.\n{lines}'
            print(message)
            raise ValueError(message)
        return without_dir

    def validate_name_created(self, expected_md, created_name):
        if created_name != expected_md:
            print(f'created: {created_name} {len(created_name)}')
            print(f'expected: {expected_md} {len(expected_md)}')
            print([created_name]) # this will show hidden characters
            message = f'Error: created file {created_name} does not match current name {expected_md}'
            print(message)
            raise ValueError(message)
        print(created_name)

    def create_a_new_article(self, article_name):
        r"""
        create a new article by specified name
        """
        expected_md = f'{article_name}.md'
        command = self.command_new(article_name)
        if self.dry_run:
            created = self.example_stdout_at_new(expected_md)
            print(f'DRY_RUN: skipping creating new article file.\n{command}')
        else:
            result = Run.run_command(self.local_path(), command, return_result=True)
            print(result.returncode)
            print(result.stderr)
            print(result.stdout)
            created = result.stdout

        created_name = self.extract_name_created(created)
        self.validate_name_created(expected_md, created_name)

    def remove_doc(self, article_path):
        r"""
        remove document body from current article
        """
        # remove lines after the 2nd `---`
        if self.dry_run:
            print(f'DRY_RUN: skipping remove document from {article_path}')
        else:
            with open(article_path, 'r') as file:
                current_content = file.readlines()

            # check the 1st
            if not self.is_separator_line(current_content[0]):
                message = f'Error: broken content. 1st line must be a separator. {current_content[0]}'
                print(message)
                raise ValueError(message)

            # search the 2nd
            head_content = [current_content[0]]
            detected = False
            for line in current_content[1:]:
                head_content.append(line)
                if self.is_separator_line(line):
                    detected = True
                    print('2nd separator is detected.')
                    break

            # it still allows head only document (blank new),
            # but a head only one also has the 2nd separator.
            if not detected:
                message = f'Error: broken content. No 2nd separator.'
                print(head_content)
                print(message)
                raise ValueError(message)

            # overwrite the document with head
            with open(article_path, 'w') as file:
                file.writelines(head_content)

    def update_doc(self, article_path, base_doc):
        r"""
        insert base_doc into current article
        """
        if self.dry_run:
            print(f'DRY_RUN: skipping append {base_doc} to {article_path}')
        else:
            with open(base_doc, 'r') as base_file:
                base_content = base_file.read()
                with open(article_path, 'a') as file:
                    file.write(self.transform_doc_md(base_content))

    def update_meta(self, article_path):
        r"""
        update meta information of current article
        """
        meta = self.create_meta_head(article_path)
        if self.dry_run:
            print(f'DRY_RUN: skipping update meta information')
        else:
            with open(article_path, 'w') as file:
                file.write(meta)

    def new_article(self):
        r"""
        create a new article document
        """
        article_name = self.article_name()
        # caution: zenn changes this name on every call.
        # sure to use this local variable before file creation.

        self.create_a_new_article(article_name)

        # this should be after the file creation, to avoid creating another name
        article_path = self.article_path()
        print(article_path)

        if self.dry_run or self.no_git:
            print('DRY_RUN: skipping git add')
        else:
            self.git().git_add(article_path)

        return True

    def update_from_base(self):
        r"""
        update current article file from base
        """
        article_path = self.article_path()
        base_doc = conf_current.a_path()

        self.print_file_head(article_path, 'BEFORE')

        self.remove_doc(article_path)
        self.print_file_head(article_path, 'AFTER REMOVE BODY')

        self.update_meta(article_path)
        self.print_file_head(article_path, 'AFTER UPDATE META')

        self.update_doc(article_path, base_doc)
        self.print_file_head(article_path, 'AFTER UPDATE DOC')

        if self.dry_run or self.no_git:
            print('DRY_RUN: skipping git add')
        else:
            #self.git().git_add(article_path)
            # no path is needed because it was already added at new
            self.git_diff().diff_and_add()

    def commit_and_push(self, message):
        r"""
        git commit and push
        """
        article_name = self.article_name()
        if self.dry_run or self.no_git:
            print('DRY_RUN: skipping git commit, push')
        else:
            self.git().git_commit(f'{message}{article_name}')
            self.git().git_push()

    def is_yaml_key(self, line, keys):
        r"""
        return True if line has any of keys as yaml key
        """
        pattern = re.compile('|'.join([f'^{k}:' for k in keys]))
        return True if re.search(pattern, line) else False

    def is_yaml_array(self, line):
        r"""
        return True if line is ` - ` including white spaces
        """
        return True if re.search(r'^\s+-\s', line) else False

    def is_blank(self, line):
        r"""
        return True if line is blank including white spaces
        """
        return True if re.search(r'^\s*$', line) else False

    def is_h1(self, line):
        r"""
        return True if line is `# ` including white spaces
        """
        return True if re.search(r'^\s*#\s', line) else False

    def is_tri_hyphen(self, line):
        r"""
        return True if line is `---` and may includes LF
        """
        return '---' == line.rstrip()

    def is_separator_line(self, line):
        r"""
        detect separator between head and body
        """
        return self.is_tri_hyphen(line)

    def print_file_head(self, path, message=''):
        r"""
        print file content until the 1st `# line` detected
        """
        print(f'=== {message}: {os.path.relpath(path, self.local_path())} ===')
        truncated = False
        if self.dry_run:
            print('DRY_RUN: skipping print file head')
        else:
            with open(path, 'r') as file:
                while True:
                    content = file.readline()
                    if not content:
                        break
                    print(content.rstrip())
                    if self.is_h1(content):
                        truncated = True
                        break
        print(f"==={' Truncated ' if truncated else ''}===")

    def print_file(self, path, message=''):
        r"""
        print file content
        """
        print(f'=== {message}: {os.path.relpath(path, self.local_path())} ===')
        if self.dry_run:
            print('DRY_RUN: skipping print file')
        else:
            with open(path, 'r') as file:
                content = file.read()
                print(content)
        print("======")

    def notify(self, message):
        r"""
        notify message
        """
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        doc = re.sub(r'\n', '\n-   ', self.__doc__)
        print(f'''---
    {message} --- {now}
    -   {doc}
    ---
    ''')

    def make_initial(self):
        r"""
        create initial document
        """
        self.notify('Begin')

        print(self.git())
        self.new_article()
        self.commit_and_push('new article: ')
        self.update_from_base()
        self.commit_and_push('update from base: ')

        self.notify('Done')

    def make_update(self):
        r"""
        update document
        """
        self.notify('Begin')

        print(self.git())
        self.update_from_base()
        self.commit_and_push('update from base: ')

        self.notify('Done')


def test1(cls):
    a = cls()
    print(f'dry_run={a.dry_run}, no_git={a.no_git}, current={a.current}')
    a = cls(dry_run=True)
    print(f'dry_run={a.dry_run}, no_git={a.no_git}, current={a.current}')
    a = cls(no_git=True)
    print(f'dry_run={a.dry_run}, no_git={a.no_git}, current={a.current}')

def test2(cls):
    a = cls(dry_run=True, no_git=True)
    print(a.git())
    print(a.git())
    print(a.git_diff())
    print(a.git_diff())

def test3(cls):
    a = cls(dry_run=True, no_git=True)
    print(a.local_path())
    print(a.article_name())
    print(a.article_path())
    print(a.command_new('my_article-123'))
    print(a.create_meta_head(article_path))
    print(a.example_stdout_at_new('my_expected.md'))

def test4(cls):
    a = cls(dry_run=True, no_git=True)
    print(a.is_yaml_key('title: any', ['title', 'tags']))
    print(a.is_yaml_key(' title: any', ['title', 'tags']))
    print(a.is_yaml_key('title : any', ['title', 'tags']))
    print(a.is_yaml_key('tags: any', ['title', 'tags']))
    print(a.is_yaml_key('name: any', ['title', 'tags']))

    print(a.is_yaml_array(' - any'))
    print(a.is_yaml_array('- any'))
    print(a.is_yaml_array(' -any'))
    print(a.is_yaml_array('     -     any'))

    print(a.is_h1('# any'))
    print(a.is_h1(' # any'))
    print(a.is_h1('#any'))
    print(a.is_h1('## any'))

    print(a.is_tri_hyphen('---'))
    print(a.is_tri_hyphen('---\n'))
    print(a.is_tri_hyphen(' ---'))
    print(a.is_tri_hyphen('--- '))
    print(a.is_tri_hyphen('----'))

    print(a.is_separator_line('---\n'))

def test5(cls):
    a = cls(dry_run=True, no_git=True)
    a.print_file_head(conf_current.a_path(), 'a_path')
    a.print_file_head(conf_current.meta_path(), 'meta_path')
    a = cls(no_git=True)
    a.print_file_head(conf_current.a_path(), 'a_path')
    a.print_file_head(conf_current.meta_path(), 'meta_path')

def test6(cls):
    a = cls(dry_run=True, no_git=True)
    a.print_file(conf_current.a_path(), 'a_path')
    a.print_file(conf_current.meta_path(), 'meta_path')
    a = cls(no_git=True)
    a.print_file(conf_current.a_path(), 'a_path')
    a.print_file(conf_current.meta_path(), 'meta_path')

def test7(cls):
    a = cls(dry_run=True, no_git=True)
    a.notify('notify')

def test8(cls):
    a = cls(dry_run=True, no_git=True)
    out = a.example_stdout_at_new('my_expected.md')
    print(out)
    print(a.extract_name_created(out))

def test9(cls):
    a = cls(dry_run=True, no_git=True)
    out = a.example_stdout_at_new('my_expected.md')
    print(a.extract_name_created(out + out))

def test10(cls):
    a = cls(dry_run=True, no_git=True)
    print(a.extract_name_created('no_created_line'))

def test11(cls):
    a = cls(dry_run=True, no_git=True)
    a.validate_name_created('abc', 'abc')
    try:
        a.validate_name_created('abc', 'abcd')
    except Exception as e:
        print(e)
    try:
        a.validate_name_created('abc', 'abc\t')
    except Exception as e:
        print(e)

def test12(cls):
    a = cls(dry_run=True, no_git=True)
    out = a.example_stdout_at_new('my_expected.md')
    print(a.transform_doc_md('# transform me!'))

def test():
  print('test launched manually.')
  cls = CommonUpdate
  test12(cls)

if __name__ == '__main__':
    test()
