# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
source "bin/test/make_backwards_compatible/includes.sh"

setup() {
  tmpfile="$(mktemp source_file_XXXXXX.py)"
}

teardown() {
  rm "$tmpfile"
}

@test "has help text" {
  run make_compatible -h
  [ "$status" -eq 0 ]
  [[ "$output" =~ "usage:" ]]
}

@test "No ConnectionError leaves file unchanged" {
  echo "maaatt" >> "$tmpfile"
  run make_compatible_32 "$tmpfile"
  grep -q '^maaatt$' "$tmpfile"
}
