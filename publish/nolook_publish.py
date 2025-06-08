#!/usr/bin/env python3

r"""
article publishing tools:
publish without preview current article file for base, zenn and qiita.
copyright 2025, hanagai

nolook_publish.py
version: June 8, 2025
"""

import argparse
from conf import *
from base_publish import BasePublish
from zenn_publish import ZennPublish
from qiita_publish import QiitaPublish
from zenn_update import ZennUpdate
from qiita_update import QiitaUpdate


def main():
    print('main launched manually.')
    description = 'publish without preview current article file for base, zenn and qiita.'
    arg_publish = 'enable publish (required)'
    arg_dry = 'disable git writing (optional)'
    arg_nomerge = 'disable merging pull request (optional)'
    arg_ignore = 'ignore uncommitted changes (optional)'
    myself = 'nolook_publish.py'

    f"""
    purpose:
        {description}

    usage:
        ./{myself} -- publish
        ./{myself} --publish --dry
        ./{myself} --publish --nomerge
        ./{myself} --publish --ignore

    arguments:
        --publish: {arg_publish}
        -d: {arg_dry}
        -n: {arg_nomerge}
        -i: {arg_ignore}
    """

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--publish', help=arg_publish, default=False, action='store_true')
    parser.add_argument('-d', '--dry', help=arg_dry, default=False, action='store_true')
    parser.add_argument('-n', '--nomerge', help=arg_nomerge, default=False, action='store_true')
    parser.add_argument('-i', '--ignore', help=arg_ignore, default=False, action='store_true')
    args = parser.parse_args()

    print(args)

    # require explicit --publish to prevent accidental execution
    if not args.publish:
        print("No publish action specified. Exiting.")
        print(f"Usage: ./{myself} --publish")
        return

    # at least, base file should be written
    if not conf_current.has_base_file():
        print("No current article file found for base. Exiting.")
        print(f"current key: {conf_current.get_current('key')}")
        return

    # Zenn, make initial or update
    zenn_make = ZennUpdate(dry_run=args.dry, pager=False)
    if conf_current.has_zenn_file():
        zenn_make.make_update()
    else:
        zenn_make.make_initial()

    # Qiita, make initial or update
    qiita_make = QiitaUpdate(dry_run=args.dry, pager=False)
    if conf_current.has_qiita_file():
        qiita_make.make_update()
    else:
        qiita_make.make_initial()

    # publish all
    for cls in [BasePublish, ZennPublish, QiitaPublish]:
        cls(dry_run=args.dry, no_merge=args.nomerge, ignore_uncommitted_change=args.ignore).publish()

if __name__ == '__main__':
    main()
