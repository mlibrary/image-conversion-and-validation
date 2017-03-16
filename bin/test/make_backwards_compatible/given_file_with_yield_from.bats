# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
source "bin/test/make_backwards_compatible/includes.sh"

setup() {
  tmpfile="$(mktemp source_file_XXXXXX.py)"
  echo "class SomeClass:" >> "$tmpfile"
  echo "    def __iter__ (self):" >> "$tmpfile"
  echo "        yield one_thing" >> "$tmpfile"
  echo "        yield from many_things" >> "$tmpfile"
  echo "        yield from_this" >> "$tmpfile"
  echo "        yield another_thing" >> "$tmpfile"
}

teardown() {
  rm "$tmpfile"
}

make_compatible_326() {
  make_compatible --version 3.2.6 "$@"
}

@test "Replace 'yield from' with ugly equivalent" {
  run make_compatible_326 "$tmpfile"
  [ "$status" -eq 0 ]
  not_grep 'yield from ' "$tmpfile"
  grep -q 'yield from_this' "$tmpfile"
  grep -q 'for [^ ]\+ in many_things: yield ' "$tmpfile"
}
