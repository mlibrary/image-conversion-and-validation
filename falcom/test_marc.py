# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .marc import *

class NothingTest (unittest.TestCase):

    def test_nothing (self):
        marc_data = get_marc_data_from_xml(None)
        assert_that(marc_data, has_key("bib"))
        assert_that(marc_data, has_key("callno"))
        assert_that(marc_data, has_key("oclc"))
        assert_that(marc_data, has_key("author"))
        assert_that(marc_data, has_key("title"))
        assert_that(marc_data, has_key("description"))
        assert_that(marc_data, has_key("years"))

if __name__ == "__main__":
    unittest.main()
