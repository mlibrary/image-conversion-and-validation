# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from os import environ
from unittest import skipUnless

SLOW_TESTS = environ.get("SLOW_TESTS", False)
slow_test = skipUnless(SLOW_TESTS, "slow test")
