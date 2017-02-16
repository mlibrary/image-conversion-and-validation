# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

@test "Script is executable" {
  run ./bin/auto_process_reject_lists
  [ "$status" -eq 0 ]
}
