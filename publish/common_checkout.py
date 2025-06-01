#!/usr/bin/env python3

r"""
article publishing tools:
base class to checkout article published
copyright 2025, hanagai

common_checkout.py
version: June 1, 2025
"""

import os.path
import datetime
import re
from conf import *

class CommonCheckout:
    r"""
    base class to checkout article published
    """

    memories = ['series', 'key', 'now', 'name']
    dry_run = False
    _git = None

    def git(self):
        r"""
        Git Class to use in this class
        """
        if self._git is None:
            print('initialize _git')
            from common_git import CommonGit
            self._git = CommonGit(skip_initialize=self.dry_run)
        return self._git

    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    def __str__(self):
        return (
        f'{self.__class__.__name__}('
        f')'
        )

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

    def show_current(self, message=''):
        r"""
        show current values
        """
        print(f'=== {message} ===')
        for memory in self.memories:
            print(f'{memory}: {conf_current.get_current(memory)}')
        print('======')

    def new_current(self, key):
        r"""
        make other values from key
        """
        now, name = key.split('_', 1)
        series = self.find_series_from_key(key)
        values = dict(zip(self.memories, [series, key, now, name]))
        print(values)
        return values

    def find_series_from_key(self, key):
        r"""
        return series for key by searching yaml files
        """
        yaml_list = conf_current.with_all_meta_yaml(self.parse_yaml_path)
        found = [x for x in yaml_list if x[0] == key]
        #print(found)
        match len(found):
            case 0:
                print(f'WARN: {key} not found in files published.')
                raise RuntimeError
            case 1:
                return found[0][1]
            case _:
                print(f'WARN: {key} found duplicated in files published.')
                print(yaml_list)
                raise RuntimeError

    def parse_yaml_path(self, yaml_path):
        r"""
        parse yaml path and return [key, series]
        """
        #docs, meta, yaml = yaml_path.rsplit(os.path.sep, 2)
        yaml = os.path.basename(yaml_path)
        meta = os.path.basename(os.path.dirname(yaml_path))
        #print([meta, yaml])
        key = re.sub(r'\.yaml$', '', yaml)
        series = re.sub(r'^met', '', meta)
        values = [key, series]
        #print(values)
        return values

    def set_current(self, key):
        r"""
        set current for the key
        """
        print(f'checkout: {key}')
        self.show_current('BEFORE')

        if conf_current.get_current('key') == key:
            print(f'Skip writing: {key} is already current key')
        else:
            updates = self.new_current(key)
            if self.dry_run:
                print('DRY-RUN: not change current')
            else:
                for memory in self.memories:
                    conf_current.set_current(memory, updates[memory])
                self.show_current('AFTER')

    def checkout(self, key):
        r"""
        checkout key
        """
        self.notify('Begin')

        self.set_current(key)
        print(self.git()) # this will do checkout at initialization
        if self.git().is_danger_here():
            print('ERROR: failed to checkout')

        self.notify('Done')

def test():
    print('test launched manually.')
    dry_run = True
    #key = '70525_publish_zenn_qiita'
    key = 'not_exist'

    a = CommonCheckout(dry_run=dry_run)
    a.checkout(key)

if __name__ == '__main__':
    test()
