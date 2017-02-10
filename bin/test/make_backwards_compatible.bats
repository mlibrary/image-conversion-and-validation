# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

@test "has help text" {
  run ./bin/make_backwards_compatible -h
  [ "$status" -eq 0 ]
  [[ "$output" =~ "usage:" ]]
}
