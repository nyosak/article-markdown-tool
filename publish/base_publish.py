#!/usr/bin/env python3

r"""
article publishing tools:
publish current article file for base.
copyright 2025, hanagai

base_publish.py
version: May 30, 2025
"""

import argparse
from conf import *
from common_publish import CommonPublish

class BasePublish(CommonPublish):
    r"""
    publish current article file for base.
    """

    def git(self):
        r"""
        Git Class to use in this class
        """
        if self._git is None:
            print('initialize _git')
            from base_git import BaseGit
            self._git = BaseGit(skip_initialize=True)
        return self._git

    def article_name(self):
        r"""
        article name of target
        """
        #return conf_current.zenn_name()
        #return conf_current.qiita_name()
        return conf_current.get_current('key')


def main():
    print('main launched manually.')
    description = 'publish current article file for base.'
    arg_dry = 'disable git writing (optional)'
    arg_nomerge = 'disable merging pull request (optional)'
    arg_ignore = 'ignore uncommitted changes (optional)'
    myself = 'base_publish.py'

    f"""
    purpose:
        {description}

    usage:
        ./{myself}
        ./{myself} --dry
        ./{myself} --nomerge
        ./{myself} --ignore

    arguments:
        -d: {arg_dry}
        -n: {arg_nomerge}
        -i: {arg_ignore}
    """

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--dry', help=arg_dry, default=False, action='store_true')
    parser.add_argument('-n', '--nomerge', help=arg_nomerge, default=False, action='store_true')
    parser.add_argument('-i', '--ignore', help=arg_ignore, default=False, action='store_true')
    args = parser.parse_args()

    print(args)
    BasePublish(dry_run=args.dry, no_merge=args.nomerge, ignore_uncommitted_change=args.ignore).publish()

if __name__ == '__main__':
    main()
