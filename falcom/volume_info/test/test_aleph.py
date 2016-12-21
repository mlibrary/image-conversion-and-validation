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
EG_MARC_BUSNS = readfile("39015090867675.xml")

class TestMARCData (unittest.TestCase):

    def test_degenerate (self):
        isman = MARCData(EG_MARC_ISMAN)
        astro = MARCData(EG_MARC_ASTRO)

        self.assertEqual(isman.bib, "006822264")
        self.assertEqual(astro.bib, "002601791")

        self.assertEqual(isman.callno, "Isl. Ms. 402")
        self.assertEqual(astro.callno, "Isl. Ms. 782")

        self.assertEqual(isman.author, "")
        self.assertEqual(astro.author, "")
