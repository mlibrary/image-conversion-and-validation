# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

make_compatible() {
  ./bin/make_backwards_compatible "$@"
}

not_grep() {
  if grep -q "$@"; then false; else true; fi
}
