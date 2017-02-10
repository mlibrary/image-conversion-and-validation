# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

setup() {
  tmpfile="$(mktemp source_file_XXXXXX.py)"
}

teardown() {
  rm "$tmpfile"
}

make_compatible() {
  ./bin/make_backwards_compatible "$@"
}

@test "has help text" {
  run make_compatible -h
  [ "$status" -eq 0 ]
  [[ "$output" =~ "usage:" ]]
}

@test "ConnectionError becomes OSError in <3.3" {
  echo "except ConnectionError:"  >> "$tmpfile"
  echo "    pass"                 >> "$tmpfile"
  run make_compatible --version 3.2.5 "$tmpfile"
  [ "$status" -eq 0 ]
  ! grep -q ConnectionError "$tmpfile"
  grep -q '^except OSError:$' "$tmpfile"
}

@test "No ConnectionError leaves file unchanged" {
  echo "maaatt" >> "$tmpfile"
  run make_compatible --version 3.2.5 "$tmpfile"
  grep -q '^maaatt$' "$tmpfile"
}
