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
  echo "        yield another_thing" >> "$tmpfile"
}

teardown() {
  rm "$tmpfile"
}

make_compatible_326() {
  make_compatible --version 3.2.5 "$@"
}

@test "working test environment" {
  true
}
