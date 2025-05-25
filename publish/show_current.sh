#!/bin/sh
# article publishing tools:
# show current settings
# copyright 2025, hanagai
#
# show_current.sh
# version: May 25, 2025

parent_dir=$(dirname "$(realpath "$0")")

for f in `ls -1 $parent_dir/../tmp/current_*`
do
  echo -n "- $(basename "$f"): "
  cat $f
  echo ""
done
