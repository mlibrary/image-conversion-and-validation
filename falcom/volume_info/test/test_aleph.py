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

class TestMARCData (unittest.TestCase):

    def assert_marc_values (self, xml_data, **kwargs):
        marc = MARCData(xml_data)

        for key, value in kwargs.items():
            self.assertEqual(getattr(marc, key), value)

    def test_isman_xml (self):
        self.assert_marc_values(EG_MARC_ISMAN,
                bib="006822264",
                callno="Isl. Ms. 402",
                author=None,
                title="[Calligraphic specimen,",
                description=None,
                years=("1790", "1791"))

    def test_astro_xml (self):
        self.assert_marc_values(EG_MARC_ASTRO,
                bib="002601791",
                callno="Isl. Ms. 782",
                author=None,
                title="Astronomical tables :",
                description=None,
                years=("16uu", None))

    def test_business_xml (self):
        self.assert_marc_values(EG_MARC_BUSINESS,
                bib="011694516",
                callno="LD755.A87 P45 2012",
                author="Pelfrey, Patricia A.",
                title="Entrepreneurial president :",
                description=None,
                years=("2012", None))
