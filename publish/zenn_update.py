#!/usr/bin/env python3

r"""
article publishing tools:
create and update an article file for zenn.
copyright 2025, hanagai

zenn_update.py
version: May 28, 2025
"""

import argparse
from conf import *
from common_run import Run
from common_update import CommonUpdate

class ZennUpdate(CommonUpdate):
    r"""
    create and update an article file for zenn.
    """

    def git(self):
        r"""
        Git Class to use in this class
        """
        if self._git is None:
            print('initialize _git')
            from zenn_git import ZennGit
            self._git = ZennGit(skip_initialize=self.dry_run)
        return self._git

    def git_diff(self):
        r"""
        Git Diff Class to use in this class
        """
        if self._git_diff is None:
            print('initialize _git_diff')
            from zenn_diff import ZennDiff
            self._git_diff = ZennDiff(dry_run=self.dry_run)
        return self._git_diff

    def local_path(self):
        r"""
        local repo path to use in this class
        """
        return conf_dirs.ZENN

    def article_name(self):
        r"""
        article name of target
        """
        return conf_current.zenn_name()

    def article_path(self):
        r"""
        article path of target
        """
        return conf_current.zenn_path()

    def command_new(self, article):
        r"""
        command to generate a new article
        """
        return ['npx', 'zenn', 'new:article', '--slug', article]

    def create_meta_head(self, article_path=None):
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


def main():
  print('main launched manually.')
  description = 'update an article file for zenn.'
  arg_dry = 'disable file writing and git (optional)'
  arg_nogit = 'disable git (optional)'
  myself = 'zenn_update.py'

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
  ZennUpdate(dry_run=args.dry,no_git=args.nogit).make_update()

if __name__ == '__main__':
    main()
