#!/bin/sh
# article publishing tools:
# preview Zenn
# copyright 2025, hanagai
#
# zenn_preview.sh
# version: May 27, 2025

parent_dir=$(dirname "$(realpath "$0")")
cd "$parent_dir/../../article-zenn-doc"
pwd

npx zenn preview
