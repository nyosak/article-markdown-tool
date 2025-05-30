#!/usr/bin/env python3

r"""
article publishing tools:
base class to publish current article
copyright 2025, hanagai

common_publish.py
version: May 30, 2025
"""

import datetime
import re
from conf import *

class CommonPublish:
    r"""
    base class to publish current article
    """

    dry_run = False
    no_merge=False
    ignore_uncommitted_change=False
    _git = None

    def git(self):
        r"""
        Git Class to use in this class
        """
        if self._git is None:
            print('initialize _git')
            from common_git import CommonGit
            self._git = CommonGit(skip_initialize=True)
        return self._git

    def article_name(self):
        r"""
        article name of target
        """
        #return conf_current.zenn_name()
        #return conf_current.qiita_name()
        return conf_current.get_current('key')

    def __init__(self, dry_run=False, no_merge=False, ignore_uncommitted_change=False):
        # dry_run disables publishing
        self.dry_run = dry_run
        self.no_merge = no_merge
        self.ignore_uncommitted_change = ignore_uncommitted_change

    def __str__(self):
        return (
        f'{self.__class__.__name__}('
        f'{self.article_name()},'
        f'{self.git()},'
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

    def no_branch(self):
        r"""
        return True if not local branch found
        """
        return not self.git().git_exists_branch()

    def has_uncommitted_change(self):
        r"""
        return True if target repo has uncommitted changes
        """
        print('Checking uncommitted changes.')

        status = self.git().git_status_short(with_branch=True)
        lines = status.split('\n')
        #print(lines)
        branch_info = lines[0].split()
        # ## main...origin/main [ahead 11]
        # ## 70525_publish_zenn_qiita
        current_branch = re.sub(r'\..*$', '', branch_info[1])

        if current_branch != self.git().branch():
            print(f'SKIP checking: current branch {current_branch} is not the target branch.')
            return False

        has_ahead = len(branch_info) > 2
        has_changes = lines[1] != ''

        if not (has_ahead or has_changes):
            print('Good: status is clear.')
            return False

        if self.ignore_uncommitted_change:
            print(f'SKIP checking: ignore_uncommitted_change option is True.')
            return False

        if has_ahead:
            print('WARN: may have to push before publishing.')
            return True

        if has_changes:
            print('WARN: uncommitted changes detected.')
            return True

    def has_pull_request(self):
        r"""
        return True if there is a pull request opened.
        """
        pr_exists = self.git().git_has_open_pull_request()
        if pr_exists:
            print('Already has pull request opened.')
        return pr_exists

    def create_pull_request(self):
        r"""
        create a new pull request
        """
        if self.dry_run:
            print('DRY_RUN: no creating')
        else:
            print('creating a new pull request')
            out = self.git().git_create_pull_request(self.article_name())
            if out == False:
                raise RuntimeError('Error: creating pull request failed')
            else:
                print(out)

    def merge_pull_request(self):
        r"""
        merge pull request for current article
        """
        if self.dry_run:
            print('DRY_RUN: no merging')
        else:
            pr = self.git().git_current_pull_request()
            pr_number = pr['number']
            print(f'merging pull request #{pr_number}')
            if self.no_merge:
                print(f'NO_MERGE: no merging')
                print(f'pull request: {pr["url"]}')
            else:
                self.git().git_merge_pull_request(pr_number)
                print('merged')

    def publish(self):
        r"""
        publish current article
        """
        self.notify('Begin')
        repo = f'{self.git().repo_name()}:{self.git().branch()}'

        if self.no_branch():
            print(f'SKIP: no branch found. Already merged? {repo}')
            self.notify('Done')
            return

        if self.has_uncommitted_change():
            raise RuntimeError(f'Error: {repo} has uncommitted changes.')

        if not self.has_pull_request():
            self.create_pull_request()

        self.merge_pull_request()

        self.notify('Done')


def test():
    print('test launched manually.')
    dry_run = True
    no_merge = True
    ignore_uncommitted_change = False

    a = CommonPublish(dry_run=dry_run, no_merge=no_merge, ignore_uncommitted_change=ignore_uncommitted_change)
    a.publish()

if __name__ == '__main__':
    test()
