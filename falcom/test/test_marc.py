# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import os
import unittest
import xml.etree.ElementTree as ET

from ..marc import *
from .hamcrest_marc import ComposedAssertion, \
        has_marc_attrs, evaluates_to_true, evaluates_to_false

FILE_BASE = os.path.join(os.path.dirname(__file__), "files")

def readfile (filename):
    with open(os.path.join(FILE_BASE, filename), "r") as f:
        result = f.read()

    return result

EG_MARC_ISMAN = readfile("39015079130699.xml")
EG_MARC_ASTRO = readfile("39015081447313.xml")
EG_MARC_BUSINESS = readfile("39015090867675.xml")
EG_MARC_MIDAILY = readfile("39015071755826.xml")

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

class MARCDataTest (unittest.TestCase):

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

    def test_correct_marc_data_from_isman_xml (self):
        marc = get_marc_data_from_xml(EG_MARC_ISMAN)

        assert_that(marc, evaluates_to_true())

if __name__ == "__main__":
    unittest.main()
