# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import os
import unittest
import xml.etree.ElementTree as ET

from ..marc import *
from .hamcrest import ComposedAssertion
from .hamcrest_marc import \
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

EG_MARC_AUTHOR_110 = readfile("39015084510513.xml")
EG_MARC_AUTHOR_111 = readfile("author_111_39015090867675.xml")
EG_MARC_AUTHOR_130 = readfile("author_130_39015090867675.xml")

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

def has_marc_data(**kwargs):
    return IsParticularMarcData(True, **kwargs)

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
        assert_that(get_marc_data_from_xml(EG_MARC_ISMAN),
                    has_marc_data(bib="006822264",
                                  callno="Isl. Ms. 402",
                                  author=None,
                                  title="[Calligraphic specimen,",
                                  description=None,
                                  years=("1790", "1791"),
                                  oclc=None))

    def test_correct_marc_data_from_astro_xml (self):
        assert_that(get_marc_data_from_xml(EG_MARC_ASTRO),
                    has_marc_data(bib="002601791",
                                  callno="Isl. Ms. 782",
                                  author=None,
                                  title="Astronomical tables :",
                                  description=None,
                                  years=("16uu", None),
                                  oclc="706055947"))

    def test_correct_marc_data_from_business_xml (self):
        assert_that(get_marc_data_from_xml(EG_MARC_BUSINESS),
                    has_marc_data(bib="011694516",
                                  callno="LD755.A87 P45 2012",
                                  author="Pelfrey, Patricia A.",
                                  title="Entrepreneurial president :",
                                  description=None,
                                  years=("2012", None),
                                  oclc="756167029"))

    def test_correct_marc_data_from_midaily_xml (self):
        assert_that(get_marc_data_from_xml(EG_MARC_MIDAILY),
                    has_marc_data(bib="002751011",
                                  callno="FImu F3g Outsize",
                                  author=None,
                                  title="The Michigan daily.",
                                  description="1927 Sept 20 - 1928 Jan 8",
                                  years=("1903", "9999"),
                                  oclc="009651208"))

    def test_author_can_pull_from_datafield_110 (self):
        assert_that(get_marc_data_from_xml(EG_MARC_AUTHOR_110),
                    has_marc_data(author="Chiusi. Museo Etrusco."))

    def test_author_can_pull_from_datafield_111 (self):
        assert_that(get_marc_data_from_xml(EG_MARC_AUTHOR_111),
                    has_marc_data(author="Pelfrey, Patricia A."))

    def test_author_can_pull_from_datafield_130 (self):
        assert_that(get_marc_data_from_xml(EG_MARC_AUTHOR_130),
                    has_marc_data(author="Pelfrey, Patricia A."))

if __name__ == "__main__":
    unittest.main()
