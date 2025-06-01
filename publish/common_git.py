#!/usr/bin/env python3

r"""
article publishing tools:
base class to handle GitHub repositories.
copyright 2025, hanagai

common_git.py
version: June 1, 2025
"""

import os.path
import json
from conf import *
from common_run import Run

class CommonGit:
  r"""
  base class to handle GitHub repositories.
  """

  def local_path(self):
    return conf_dirs.BASE
    #return 'using test repository path is recommended on development and test.'

  def account_name(self):
    return os.path.basename(os.path.dirname(self.local_path()))
    #return 'nyosak'

  def repo_name(self):
    return os.path.basename(self.local_path())
    #return 'article-base-doc'

  def repo_url(self):
    account_prefix = f'{self.account_name()}@' if self.account_name() else ''
    repo_dir = f'{self.account_name()}/{self.repo_name()}'
    return f'https://{account_prefix}github.com/{repo_dir}.git'

  def io_url(self):
    return f'https://{self.account_name()}.github.io/{self.repo_name()}/'
    #return 'https://nyosak.github.io/article-base-doc/'

  def branch(self):
    return conf_current.get_current('key')
    #return self.main_branch()
    #return 'testing2'

  def main_branch(self):
    return 'main'
    #return 'testing'

  def enabled(self):
    return True

  def enable_create_branch(self):
    return True

  def enable_delete_branch(self):
    return True

  def enable_pull(self):
    return True

  def enable_add(self):
    return True

  def enable_commit(self):
    return True

  def enable_push(self):
    return True

  def enable_pull_request(self):
    # requires GitHub CLI
    return True

  def is_danger_here(self):
    # prohibit adding another branch
    current_branch = self.git_current_branch()
    target_branch = self.branch()
    danger = current_branch != target_branch
    if danger:
      print(f'WARN: current branch {current_branch} is not {target_branch}')
    return danger

  def __init__(self, skip_initialize=False):
    if skip_initialize:
      return
    self.git_status()
    self.git_pull_main()
    self.git_checkout()
    self.git_pull()
    self.git_status_short()

  def __str__(self):
    return (
      f'{self.__class__.__name__}('
      f'{self.repo_name()},'
      f'{self.local_path()},'
      f'{self.repo_url()},'
      f'{self.account_name()},'
      f'{self.branch()},'
      f')'
    )

  def run_command(self, command, return_result=False):
    cwd = self.local_path()
    return Run.run_command(cwd, command, return_result)

  def relative_path(self, file):
    if os.path.isabs(file):
      return os.path.relpath(file, self.local_path())
    else:
      return file

  def git_pull_main(self):
    if self.enabled() and self.enable_pull():
      return self.run_command(['git', 'pull', self.repo_url(), self.main_branch()])
    else:
      return True

  def git_pull(self):
    if self.enabled() and self.enable_pull() and self.git_exists_remote_branch():
      return self.run_command(['git', 'pull', self.repo_url(), self.branch()])
    else:
      return True

  def git_status(self):
    if self.enabled():
      return self.run_command(['git', 'status'])
    else:
      return True

  def git_status_short(self, with_branch=False):
    if self.enabled():
      command = ['git', 'status', '-s']
      if with_branch:
        command.append('-b')
      result = self.run_command(command, return_result=True)
      return result.stdout
    else:
      return True

  def git_checkout(self, create_if_required=True):
    if self.enabled() and self.enable_add():
      if not self.git_exists_branch():
        if create_if_required and self.enable_create_branch():
          self.git_create_branch()
        else:
          print(f'branch {self.branch()} does not exist.')
          return False
      return self.run_command(['git', 'checkout', self.branch()])
    else:
      return True

  def git_add(self, file):
    if self.enabled() and self.enable_add():
      if self.is_danger_here():
        raise RuntimeError('Error: prohibit git add to this branch')
      return self.run_command(['git', 'add', self.relative_path(file)])
    else:
      return True

  def git_add_u(self):
    if self.enabled() and self.enable_add():
      if self.is_danger_here():
        raise RuntimeError('Error: prohibit git add to this branch')
      return self.run_command(['git', 'add', '-u'])
    else:
      return True

  def git_commit(self, message):
    if self.enabled() and self.enable_commit():
      if self.is_danger_here():
        raise RuntimeError('Error: prohibit git commit to this branch')
      return self.run_command(['git', 'commit', '-m', message])
    else:
      return True

  def git_push(self):
    if self.enabled() and self.enable_push():
      if self.is_danger_here():
        raise RuntimeError('Error: prohibit git push to this branch')
      return self.run_command(['git', 'push', '-u', self.repo_url(), self.branch()])
    else:
      return True

  def git_current_branch(self):
    if self.enabled():
      result = self.run_command(['git', 'branch', '--show-current'], return_result=True)
      return result.stdout.strip()

  def git_exists_branch(self):
    if self.enabled():
      result = self.run_command(['git', 'branch', '--list', self.branch()], return_result=True)
      return len(result.stdout.strip()) > 0
    else:
      return True

  def git_exists_remote_branch(self):
    if self.enabled():
      result = self.run_command(['git', 'branch', '--remote', '--list', f'origin/{self.branch()}'], return_result=True)
      return len(result.stdout.strip()) > 0
    else:
      return True

  def git_create_branch(self):
    if self.enabled() and self.enable_create_branch():
      return self.run_command(['git', 'branch', self.branch(), self.main_branch()])
    else:
      return True

  def git_delete_branch(self):
    if self.enabled() and self.enable_delete_branch():
      if self.git_exists_branch():
        return self.run_command(['git', 'branch', '-D', self.branch()])
      else:
        print(f'branch {self.branch()} does not exist.')
        return True
    else:
      return True

  def git_delete_remote_branch(self):
    if self.enabled() and self.enable_delete_branch():
      if self.git_exists_remote_branch():
        return self.run_command(['git', 'push', self.repo_url(), '--delete', self.branch()])
      else:
        print(f'remote branch {self.branch()} does not exist.')
        return True
    else:
      return True

  def git_create_pull_request(self, body='required'):
    if self.enabled() and self.enable_pull_request():
      base = self.main_branch()
      head = self.branch()
      title = f'{head} to {base}'
      command = ['gh', 'pr', 'create', '--title', title, '--base', base, '--head', head, '--body', body]

      result = self.run_command(command, return_result=True)

      if result is False:
        print('Failed to create pull request.')
        return False
      elif result.returncode != 0:
        print(f'Error creating pull request: {result.returncode}: {result.stderr.strip()}')
        return False
      else:
        return result.stdout.strip()
    else:
      return True

  def git_current_pull_request(self):
    if self.enabled() and self.enable_pull_request():
      result = self.run_command(
        ['gh', 'pr', 'status',
          '--jq', f'.currentBranch | select(.baseRefName=="{self.main_branch()}" and .state=="OPEN")',
          '--json', 'id,number,url,state,closed,baseRefName,headRefName'
        ], return_result=True)
      parsed_result = json.loads(result.stdout.strip()) if result.returncode == 0 and result.stdout.strip() != '' else {'error': result.returncode}
      return parsed_result
    else:
      return True

  def git_has_open_pull_request(self):
    if self.enabled() and self.enable_pull_request():
      pr = self.git_current_pull_request()
      if isinstance(pr, dict) and 'error' not in pr:
        return True
      else:
        return False
    else:
      return True

  def git_current_pull_request_number(self):
    if self.enabled() and self.enable_pull_request():
      pr = self.git_current_pull_request()
      if isinstance(pr, dict) and 'number' in pr:
        return pr['number']
      else:
        return None
    else:
      return True

  def git_merge_pull_request(self, pr_number=None):
    if self.enabled() and self.enable_pull_request():
      if pr_number is None:
        pr_number = self.git_current_pull_request_number()
      if pr_number is not None:
        return self.run_command(['gh', 'pr', 'merge', str(pr_number), '--merge', '--delete-branch'])
      else:
        print('No pull request number provided.')
        return False
    else:
      return True


# Test function to demonstrate usage
def test():
  print('test launched manually.')
  a = CommonGit()
  b = CommonGit(skip_initialize=True)
  print(a)
  print(b)
  print(a.relative_path('/home/kuro/app_doc/nyosak/article-base-doc/docs/a/70523_publish_zenn_qiita.md'))
  print(b.relative_path('home/kuro/app_doc/nyosak/article-base-doc/docs/a/70523_publish_zenn_qiita.md'))
  print(a.git_current_branch())
  print(a.git_exists_branch())
  print(a.git_exists_remote_branch())

  if a.main_branch() != 'main':
    print(a.git_add('test1.notexist'))
    print(a.git_commit('test commit'))
    print(a.git_push())
    print(a.git_create_pull_request('test pull request body'))
    print(a.git_current_pull_request())
    print(a.git_has_open_pull_request())
    print(a.git_current_pull_request_number())
    #print(a.git_merge_pull_request(1234567))
    print(a.git_merge_pull_request())
    print(a.git_delete_branch())
    print(a.git_delete_remote_branch())

if __name__ == '__main__':
  test()
