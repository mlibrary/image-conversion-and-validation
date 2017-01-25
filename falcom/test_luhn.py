# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .luhn import get_check_digit

class Nothing (unittest.TestCase):

    def test_working_test_environment (self):
        pass
