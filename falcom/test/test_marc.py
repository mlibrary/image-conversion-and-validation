# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest
import xml.etree.ElementTree as ET

from ..marc import *
from .hamcrest_marc import ComposedAssertion, \
        has_marc_attrs, evaluates_to_true, evaluates_to_false

class IsParticularMarcData (ComposedAssertion):

    def __init__ (self, eval_to_true = True, **kwargs):
        self.eval_to_true = eval_to_true
        self.kwargs = kwargs

    def assertion (self, item):
        if self.eval_to_true:
            yield evaluates_to_true()

        else:
            yield evaluates_to_false()

        yield has_marc_attrs(**self.kwargs)

def is_empty_marc_data():
    return IsParticularMarcData(False,
                                bib=None,
                                callno=None,
                                oclc=None,
                                author=None,
                                title=None,
                                description=None,
                                years=(None, None))

class NothingTest (unittest.TestCase):

    def test_marc_data_of_None_yields_empty_MARC_data (self):
        assert_that(get_marc_data_from_xml(None),
                    is_empty_marc_data())

    def test_marc_data_of_empty_str_yields_empty_MARC_data (self):
        assert_that(get_marc_data_from_xml(""),
                    is_empty_marc_data())

    def test_marc_data_of_empty_xml_yields_empty_MARC_data (self):
        empty_etree = ET.fromstring("<empty/>")

        assert_that(get_marc_data_from_xml(empty_etree),
                    is_empty_marc_data())

if __name__ == "__main__":
    unittest.main()
