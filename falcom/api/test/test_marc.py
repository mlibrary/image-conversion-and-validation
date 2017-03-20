# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import os
import unittest
import xml.etree.ElementTree as ET

from ...test.hamcrest import ComposedMatcher, HasAttrs, evaluates_to
from ...test.read_example_file import ExampleFileTest
from ..marc import *

class MarcFileTest (ExampleFileTest):
    this__file__ = __file__
    format_str = "{}.xml"

    def assert_yields_marc_data (self, *args, **kwargs):
        assert_that(self.file_data, yields_marc_data(*args, **kwargs))

FILE_BASE = os.path.join(os.path.dirname(__file__), "files")

def readfile (filename):
    with open(os.path.join(FILE_BASE, filename), "r") as f:
        result = f.read()

    return result

EG_MARC_AUTHOR_110 = readfile("39015084510513.xml")
EG_MARC_AUTHOR_111 = readfile("author_111_39015090867675.xml")
EG_MARC_AUTHOR_130 = readfile("39015050666182.xml")

def has_marc_attrs(**kwargs):
    return HasAttrs("MARC attrs", **kwargs)

class YieldsParticularMarcData (ComposedMatcher):

    def __init__ (self, eval_to_true = True, **kwargs):
        self.eval_to_true = eval_to_true
        self.kwargs = kwargs

    def assertion (self, item):
        data = get_marc_data_from_xml(item)

        if self.eval_to_true:
            yield data, evaluates_to(True)

        else:
            yield data, evaluates_to(False)

        yield data, has_marc_attrs(**self.kwargs)

def yields_marc_data(**kwargs):
    return YieldsParticularMarcData(True, **kwargs)

def yields_empty_marc_data():
    return YieldsParticularMarcData(False,
                                    bib=None,
                                    callno=None,
                                    oclc=None,
                                    author=None,
                                    title=None,
                                    description=None,
                                    years=(None, None))

class GivenIslamicManuscriptXML (MarcFileTest):
    filename = "39015079130699"

    def test_correct_marc_data_from_isman_xml (self):
        self.assert_yields_marc_data(
                        bib="006822264",
                        callno="Isl. Ms. 402",
                        author=None,
                        title="[Calligraphic specimen,",
                        description=None,
                        years=("1790", "1791"),
                        oclc=None)

class GivenAstronomyXML (MarcFileTest):
    filename = "39015081447313"

    def test_correct_marc_data_from_astro_xml (self):
        self.assert_yields_marc_data(
                        bib="002601791",
                        callno="Isl. Ms. 782",
                        author=None,
                        title="Astronomical tables :",
                        description=None,
                        years=("16uu", None),
                        oclc="706055947")

class GivenBusinessXML (MarcFileTest):
    filename = "39015090867675"

    def test_correct_marc_data_from_business_xml (self):
        self.assert_yields_marc_data(
                        bib="011694516",
                        callno="LD755.A87 P45 2012",
                        author="Pelfrey, Patricia A.",
                        title="Entrepreneurial president :",
                        description=None,
                        years=("2012", None),
                        oclc="756167029")

class GivenMichiganDailyXML (MarcFileTest):
    filename = "39015071755826"

    def test_correct_marc_data_from_midaily_xml (self):
        self.assert_yields_marc_data(
                        bib="002751011",
                        callno="FImu F3g Outsize",
                        author=None,
                        title="The Michigan daily.",
                        description="1927 Sept 20 - 1928 Jan 8",
                        years=("1903", "9999"),
                        oclc="009651208")

class GivenAuthorInDatafield110 (MarcFileTest):
    filename = "39015084510513"

    def test_can_pull_author (self):
        self.assert_yields_marc_data(author="Chiusi. Museo Etrusco.")

class MARCDataTest (unittest.TestCase):

    def test_marc_data_of_None_yields_empty_MARC_data (self):
        assert_that(None, yields_empty_marc_data())

    def test_marc_data_of_empty_str_yields_empty_MARC_data (self):
        assert_that("", yields_empty_marc_data())

    def test_marc_data_of_empty_xml_yields_empty_MARC_data (self):
        empty_etree = ET.fromstring("<empty/>")
        assert_that(empty_etree, yields_empty_marc_data())

    def test_author_can_pull_from_datafield_110 (self):
        assert_that(EG_MARC_AUTHOR_110, yields_marc_data(
                        author="Chiusi. Museo Etrusco."))

    def test_author_can_pull_from_datafield_111 (self):
        assert_that(EG_MARC_AUTHOR_111, yields_marc_data(
                        author="Pelfrey, Patricia A."))

    def test_author_can_pull_from_datafield_130 (self):
        assert_that(EG_MARC_AUTHOR_130, yields_marc_data(
                        author="Châtelaine de Vergi."))
