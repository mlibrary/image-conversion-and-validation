# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
source "bin/test/make_backwards_compatible/includes.sh"

setup() {
  tmpfile="$(mktemp source_file_XXXXXX.py)"
  echo "except ConnectionError:"  >> "$tmpfile"
  echo "    pass"                 >> "$tmpfile"
  echo "except BrokenPipe:"       >> "$tmpfile"
  echo "    pass"                 >> "$tmpfile"
}

teardown() {
  rm "$tmpfile"
}

@test "ConnectionError becomes OSError in <3.3" {
  run make_compatible --version 3.2.5 "$tmpfile"
  [ "$status" -eq 0 ]
  not_grep ConnectionError "$tmpfile"
  grep -q '^except OSError:$' "$tmpfile"
  grep -q '^ \+pass$' "$tmpfile"
}

@test "BrokenPipe becomes OSError in <3.3" {
  run make_compatible --version 3.2.5 "$tmpfile"
  [ "$status" -eq 0 ]
  not_grep BrokenPipe "$tmpfile"
  grep -q '^except OSError:$' "$tmpfile"
  grep -q '^ \+pass$' "$tmpfile"
}

@test "ConnectionError and BrokenPipe become OSError in <3.3" {
  run make_compatible --version 3.2.5 "$tmpfile"
  [ "$status" -eq 0 ]
  not_grep ConnectionError "$tmpfile"
  not_grep BrokenPipe "$tmpfile"
  grep -q '^except OSError:$' "$tmpfile"
  grep -q '^ \+pass$' "$tmpfile"
}

@test "ConnectionError is fine if python >=3.3" {
  run make_compatible --version 3.3.0 "$tmpfile"
  grep -q ConnectionError "$tmpfile"
}
