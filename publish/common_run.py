#!/usr/bin/env python3

r"""
article publishing tools:
run shell command in subprocess
copyright 2025, hanagai

common_run.py
version: May 27, 2025
"""

import subprocess
import sys

class Run:
  @staticmethod
  def run_command(cwd, command, return_result=False):
    print(f'at {cwd}')
    print(' '.join(command))
    try:
      result = subprocess.run(command, check=True, capture_output=True, text=True, cwd=cwd)
      print(result.stdout)
      print(result.returncode)
      if return_result:
        return result
      else:
        return True
    except subprocess.CalledProcessError as e:
      print(f'Error: {e}')
      return False

  def run_direct(cwd, command, stdout=sys.stdout, stderr=sys.stderr):
    r"""
    run command directly on sys.stdout and sys.stderr.
    will be colored, paged
    """
    print(f'at {cwd}')
    print(' '.join(command))
    try:
      return subprocess.run(command, check=True, cwd=cwd, stdout=stdout, stderr=stderr)
    except subprocess.CalledProcessError as e:
      print(f'Error: {e}')
      raise


# Test function to demonstrate usage
def test():
  print('test launched manually.')
  print(Run.run_command('.', ['echo', 'Hello, World!'], return_result=True))
  print(Run.run_command('.', ['echo', 'Hello, World!'], return_result=False))
  try:
    print(Run.run_command('.', ['ech', 'Hello, World!'], return_result=True))
  except Exception as e:
    print(f'Caught an exception: {e}')
  try:
    print(Run.run_command('./not_existing_dir', ['echo', 'Hello, World!'], return_result=True))
  except Exception as e:
    print(f'Caught an exception: {e}')
  print(Run.run_command('.', ['pwd'], return_result=True))
  print(Run.run_command('..', ['pwd'], return_result=True))
  print(Run.run_command('.', ['ls', 'not_existing_file'], return_result=True))
  print(Run.run_command('.', ['ls', 'not_existing_file'], return_result=False))

  print(Run.run_direct('.', ['ls', '-l', '--color=always']))
  print(Run.run_direct('.', ['git', 'diff']))
  #print(Run.run_direct('.', ['git', 'xxxdiff']))

if __name__ == '__main__':
  test()
