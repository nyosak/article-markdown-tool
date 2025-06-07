#!/bin/bash
# article publishing tools:
# ls at base
# copyright 2025, hanagai
#
# base_ls.sh
# version: June 7, 2025

parent_dir=$(dirname "$(realpath "$0")")
cd "$parent_dir/../../article-base-doc"
pwd

key=$1
if [ key != "" ];then
  wild=${key}'*'
else
  wild=''
fi

echo '# md'
ls docs/*/*$wild.md
echo -e "\n# yaml"
head -n 2 docs/*/*$wild.yaml
