# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import os
import unittest

from ..aleph import MARCData

FILE_BASE = os.path.join(os.path.dirname(__file__), "files")

def readfile (filename):
    with open(os.path.join(FILE_BASE, filename), "r") as f:
        result = f.read()

    return result

EG_MARC_ISMAN = readfile("39015079130699.xml")
EG_MARC_ASTRO = readfile("39015081447313.xml")
EG_MARC_BUSINESS = readfile("39015090867675.xml")
EG_MARC_MIDAILY = readfile("39015071755826.xml")

class TestMARCData (unittest.TestCase):

    def init_marc_data (self, marc_xml):
        self.marc = MARCData(marc_xml)

    def assert_marc_values (self, marc_xml, **kwargs):
        self.init_marc_data(marc_xml)

        for key, value in kwargs.items():
            self.assertEqual(getattr(self.marc, key), value)

    def assert_cant_set_attr (self, attr, value):
        with self.assertRaises(AttributeError):
            setattr(self.marc, attr, value)

    def test_isman_xml (self):
        self.assert_marc_values(EG_MARC_ISMAN,
                bib="006822264",
                callno="Isl. Ms. 402",
                author=None,
                title="[Calligraphic specimen,",
                description=None,
                years=("1790", "1791"),
                oclc=None)

    def test_astro_xml (self):
        self.assert_marc_values(EG_MARC_ASTRO,
                bib="002601791",
                callno="Isl. Ms. 782",
                author=None,
                title="Astronomical tables :",
                description=None,
                years=("16uu", None),
                oclc="706055947")

    def test_business_xml (self):
        self.assert_marc_values(EG_MARC_BUSINESS,
                bib="011694516",
                callno="LD755.A87 P45 2012",
                author="Pelfrey, Patricia A.",
                title="Entrepreneurial president :",
                description=None,
                years=("2012", None),
                oclc="756167029")

    def test_midaily_xml (self):
        self.assert_marc_values(EG_MARC_MIDAILY,
                bib="002751011",
                callno="FImu F3g Outsize",
                author=None,
                title="The Michigan daily.",
                description="1927 Sept 20 - 1928 Jan 8",
                years=("1903", "9999"),
                oclc="009651208")

    def test_cant_set_attrs (self):
        self.init_marc_data(EG_MARC_MIDAILY)

        self.assert_cant_set_attr("bib", "012345678")
        self.assert_cant_set_attr("callno", "some other callno")
        self.assert_cant_set_attr("author", "some author")
        self.assert_cant_set_attr("title", "some title")
        self.assert_cant_set_attr("description", "a book of wonders")
        self.assert_cant_set_attr("years", ("1234", "5678"))
        self.assert_cant_set_attr("oclc", "987654321")
