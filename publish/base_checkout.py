#!/usr/bin/env python3

r"""
article publishing tools:
checkout article published for base.
copyright 2025, hanagai

base_checkout.py
version: June 1, 2025
"""

import argparse
from conf import *
from common_checkout import CommonCheckout

class BaseCheckout(CommonCheckout):
    r"""
    checkout article published for base.
    """

    def git(self):
        r"""
        Git Class to use in this class
        """
        if self._git is None:
            print('initialize _git')
            from base_git import BaseGit
            self._git = BaseGit(skip_initialize=self.dry_run)
        return self._git


def main():
    print('main launched manually.')
    description = 'checkout article published for base.'
    arg_key = 'key to checkout; 70525_publish_zenn_qiita'
    arg_dry = 'disable changes (optional)'
    myself = 'base_checkout.py'

    f"""
    purpose:
        {description}

    usage:
        ./{myself} 70525_publish_zenn_qiita
        ./{myself} 70525_publish_zenn_qiita --dry

    arguments:
        1st: {arg_key}
        -d: {arg_dry}
    """

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('key', help=arg_key)
    parser.add_argument('-d', '--dry', help=arg_dry, default=False, action='store_true')
    args = parser.parse_args()

    print(args)
    BaseCheckout(dry_run=args.dry).checkout(args.key)

if __name__ == '__main__':
    main()
