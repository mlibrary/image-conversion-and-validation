# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

auto_process() {
  ./bin/auto_process_reject_lists "$@"
}

setup() {
  tmpfile="$(mktemp config-XXXXXX.cfg)"
  cat << EOF > "$tmpfile"
[somename]
dropbox = /some/path/to/dir
ignore = README.txt, something_else.txt
destination = /another/path/another/dir
EOF
}

teardown() {
  rm "$tmpfile"
}

@test "Script requires arguments" {
  run auto_process
  [ "$status" -eq 2 ]
  [[ ${lines[0]} =~ "usage:" ]]
}

@test "Can display help" {
  run auto_process -h
  [ "$status" -eq 0 ]
}
