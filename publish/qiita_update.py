#!/usr/bin/env python3

r"""
article publishing tools:
create and update an article file for qiita.
copyright 2025, hanagai

qiita_update.py
version: May 30, 2025
"""

import argparse
from conf import *
from common_run import Run
from common_update import CommonUpdate

class QiitaUpdate(CommonUpdate):
    r"""
    create and update an article file for qiita.
    """

    def git(self):
        r"""
        Git Class to use in this class
        """
        if self._git is None:
            print('initialize _git')
            from qiita_git import QiitaGit
            self._git = QiitaGit(skip_initialize=self.dry_run)
        return self._git

    def git_diff(self):
        r"""
        Git Diff Class to use in this class
        """
        if self._git_diff is None:
            print('initialize _git_diff')
            from qiita_diff import QiitaDiff
            self._git_diff = QiitaDiff(dry_run=self.dry_run)
        return self._git_diff

    def local_path(self):
        r"""
        local repo path to use in this class
        """
        return conf_dirs.QIITA

    def article_name(self):
        r"""
        article name of target
        """
        return conf_current.qiita_name()

    def article_path(self):
        r"""
        article path of target
        """
        return conf_current.qiita_path()

    def command_new(self, article):
        r"""
        command to generate a new article
        """
        return ['npx', 'qiita', 'new', article]

    def qiita_clean_head(self, current_head):
        r"""
        return head list to reuse as is for qiita
        """
        cleaned = []
        for item in current_head:
            if self.is_tri_hyphen(item):
                continue
            if self.is_h1(item):
                continue
            if self.is_blank(item):
                continue
            if self.is_yaml_array(item):
                continue
            if self.is_yaml_key(item, ['title', 'tags']):
                continue
            cleaned.append(item.rstrip())
        print(f'current: {current_head}')
        print(f'cleaned: {cleaned}')
        return cleaned

    def create_meta_head(self, article_path=None):
        r"""
        create meta information string of current article
        """
        # assuming the article body is removed before calling this.
        if self.dry_run:
            print('DRY_RUN: skipping read current article head')
            current_head = self.qiita_example_article().split('\n')
        else:
            with open(article_path, 'r') as file:
                current_head = file.readlines()
        cleaned_head = self.qiita_clean_head(current_head)
        title = self.current['title']
        tags = '\n'.join(f"  - {tag}" for tag in self.current['tags'])
        cleaned_string = '\n'.join(cleaned_head)
        meta = f"""---
title: '{title}'
tags:
{tags}
{cleaned_string}
---
"""
        print(meta)
        return meta

    def qiita_example_article(self):
        r"""
        generate mock head for dry_run, qiita
        """
        meta = f"""---
title: 'Activity, Fragment, RecyclerView について、とりあえずメモ'
tags:
  - Android
  - Activity
  - Fragment
  - RecyclerView
private: false
updated_at: '2025-02-28T09:37:20+09:00'
id: 381b3255ea2c8af21f1f
organization_url_name: null
slide: false
ignorePublish: false
---
    """
        return meta

    def example_stdout_at_new(self, expected_md):
        r"""
        mock output to use for dry_run
        """
        out = f'created: {expected_md}'
        #out = 'created: hoge.md'
        #out = "Error: 'hoge.md' is already exist"
        return out


def main():
  print('main launched manually.')
  description = 'update an article file for qiita.'
  arg_dry = 'disable file writing and git (optional)'
  arg_nogit = 'disable git (optional)'
  myself = 'qiita_update.py'

  f"""
  purpose:
    {description}

  usage:
    ./{myself}
    ./{myself} --dry
    ./{myself} --nogit

  arguments:
    -d: {arg_dry}
    -n: {arg_nogit}
  """

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-d', '--dry', help=arg_dry, default=False, action='store_true')
  parser.add_argument('-n', '--nogit', help=arg_nogit, default=False, action='store_true')
  args = parser.parse_args()

  print(args)
  QiitaUpdate(dry_run=args.dry,no_git=args.nogit).make_update()

def test():
    print('test launched manually.')
    a = QiitaUpdate(dry_run=True, no_git=True)
    print(a.qiita_example_article())
    print(a.create_meta_head())

if __name__ == '__main__':
    main()
    #test()
