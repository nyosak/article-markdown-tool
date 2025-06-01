#!/usr/bin/env python3

r"""
article publishing tools:
copy and git add pictures.
copyright 2025, hanagai

base_add_media.py
version: June 1, 2025
"""

import argparse
import datetime
import re
import os.path
import shutil
from conf import *
from common_run import Run
from base_git import BaseGit

def relative_path(file):
  r"""
  relative path from base repo
  """
  return os.path.relpath(file, conf_dirs.BASE)

def new_media_name(file):
  r"""
  make a new file name on base
  """
  new_name = conf_current.media_path(file)
  print(f'destination: {relative_path(new_name)}')
  return new_name

def copy_file(dry_run, file, dest_file):
  r"""
  copy file to dest_file
  """
  if dry_run:
    print(f'DRY-RUN: not copy {file} to {relative_path(dest_file)}')
  else:
    if file == dest_file:
      print(f'not copying, destination is same as source. {relative_path(file)}')
    else:
      shutil.copy(file, dest_file)

def git_add(dry_run, dest_file, git):
  r"""
  git add
  """
  if dry_run:
    print(f'DRY-RUN: not git add {relative_path(dest_file)}')
  else:
    git.git_add(dest_file)

def add_media_a_file(dry_run, file, git):
  r"""
  copy and git add a picture file.
  """
  dest_file = new_media_name(file)
  copy_file(dry_run, file, dest_file)
  git_add(dry_run, dest_file, git)

def notify(message):
  r"""
  notify message
  """
  now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  doc = re.sub(r'\n', '\n-   ', __doc__)
  print(f'''---
{message} --- {now}
-   {doc}
---
''')

def add_media_files(args):
  r"""
  copy and git add pictures.
  """
  notify('Begin')
  dry_run = args['dry']
  files = args['files']
  git = BaseGit(skip_initialize=dry_run)

  for file in files:
    add_media_a_file(dry_run, file, git)

  notify('Done')

def main():
  print('main launched manually.')
  description = "copy and git add pictures."
  arg_files = 'image files'
  arg_dry = 'disable file copy and git (optional)'
  myself = 'base_add_media.py'

  f"""
  purpose:
    {description}

  usage:
    ./{myself} --files ~/Pictures/image1.png ~/Downloads/image2.png
    ./{myself} --files ~/Pictures/image1.png ~/Downloads/image2.png --dry

  arguments:
    -f: {arg_files}
    -d: {arg_dry}
  """

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-f', '--files', help=arg_files, nargs='+', required=True)
  parser.add_argument('-d', '--dry', help=arg_dry, default=True, action='store_true')
  args = parser.parse_args()

  print(args)
  add_media_files(args.__dict__)

if __name__ == '__main__':
    main()

