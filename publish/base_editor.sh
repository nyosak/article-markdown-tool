#!/bin/bash
# article publishing tools:
# ls at base
# copyright 2025, hanagai
#
# base_editor.sh
# version: June 8, 2025

#editor=vi
editor='code -r'

if [ $# -eq 0 ];then
  echo "Usage: $0 [key to edit] (yaml|md)"
  echo "       $0 current md vi -R"
  exit 1
fi

parent_dir=$(dirname "$(realpath "$0")")
cd "$parent_dir/../../article-base-doc"
pwd

branch=`git branch --show-current`
if [ "$branch" != "main" ];then
  implicit_key=$branch
else
  implicit_key=''
fi

key=$1
shift
yaml=$1
shift
explicit_editor=$*

if [[ "current" == "$key"* ]];then
  if [ "$implicit_key" == "" ];then
    echo "current keyword is not available on main branch."
    exit 1
  fi
  echo "Editing current branch article. $implicit_key"
  key="$implicit_key"
fi

if [ "$yaml" != "yaml" ];then
  yaml='md'
fi

if [ "$explicit_editor" != "" ];then
  editor=$explicit_editor
fi

wild=${key}'*'

if [ "$yaml" == "yaml" ];then
  files=`ls -1 docs/*/*$wild.yaml`
else
  files=`ls -1 docs/*/*$wild.md`
fi

echo $editor $files
$editor $files
