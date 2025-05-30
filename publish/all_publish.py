#!/usr/bin/env python3

r"""
article publishing tools:
publish current article file for base, zenn and qiita.
copyright 2025, hanagai

all_publish.py
version: May 30, 2025
"""

import argparse
from conf import *
from base_publish import BasePublish
from zenn_publish import ZennPublish
from qiita_publish import QiitaPublish


def main():
    print('main launched manually.')
    description = 'publish current article file for base, zenn and qiita.'
    arg_dry = 'disable git writing (optional)'
    arg_nomerge = 'disable merging pull request (optional)'
    arg_ignore = 'ignore uncommitted changes (optional)'
    myself = 'all_publish.py'

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

    for cls in [BasePublish, ZennPublish, QiitaPublish]:
        cls(dry_run=args.dry, no_merge=args.nomerge, ignore_uncommitted_change=args.ignore).publish()

if __name__ == '__main__':
    main()
