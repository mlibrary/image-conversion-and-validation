# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

make_compatible() {
  ./bin/make_backwards_compatible "$@"
}

make_compatible_32() {
  make_compatible --version 3.2.5 "$@"
}

not_grep() {
  if grep -q "$@"; then false; else true; fi
}
