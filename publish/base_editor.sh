#!/bin/bash
# article publishing tools:
# ls at base
# copyright 2025, hanagai
#
# base_editor.sh
# version: June 7, 2025

#editor=vi
editor='code -r'

if [ $# -eq 0 ];then
  echo "Usage: $0 [key to edit] (yaml)"
  exit 1
fi

parent_dir=$(dirname "$(realpath "$0")")
cd "$parent_dir/../../article-base-doc"
pwd

key=$1
yaml=$2
wild=${key}'*'

if [ "$yaml" == "yaml" ];then
  files=`ls -1 docs/*/*$wild.yaml`
else
  files=`ls -1 docs/*/*$wild.md`
fi

echo $editor $files
$editor $files
