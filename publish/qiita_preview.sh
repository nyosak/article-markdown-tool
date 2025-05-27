#!/bin/sh
# article publishing tools:
# preview Qiita
# copyright 2025, hanagai
#
# qiita_preview.sh
# version: May 27, 2025

parent_dir=$(dirname "$(realpath "$0")")
cd "$parent_dir/../../article-qiita-doc"
pwd

npx qiita preview
