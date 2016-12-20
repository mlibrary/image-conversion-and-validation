# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import unittest

from ..str_format import *

class TestDecoyMapping (unittest.TestCase):

    def assert_keys (self, format_string, values):
        """Run get_keys_required_by_format_str and compare its result."""
        self.assertEqual(values,
                get_keys_required_by_format_str(format_string))

    def test_format_empty (self):
        self.assert_keys("no field names", set())

    def test_format_one (self):
        self.assert_keys("what if it's {hi}", {"hi"})

    def test_format_multiple (self):
        self.assert_keys("{hey} and {whatsup}", {"hey", "whatsup"})

    def test_format_decimal (self):
        self.assert_keys("{holler:d}", {"holler"})

    def test_format_float (self):
        self.assert_keys("{holler:f}", {"holler"})
