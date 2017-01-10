# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import os
import unittest

from .hamcrest import ComposedAssertion, \
        evaluates_to_false, evaluates_to_true
from ..hathi import get_oclc_counts_from_json

FILE_BASE = os.path.join(os.path.dirname(__file__), "files")

def readfile (filename):
    with open(os.path.join(FILE_BASE, filename), "r") as f:
        result = f.read()

    return result

EG_HATHI_ASTRO = readfile("hathitrust-706055947.json")
EG_HATHI_BUSINESS = readfile("hathitrust-756167029.json")
EG_HATHI_MIDAILY = readfile("hathitrust-009651208.json")

class NothingTest (unittest.TestCase):

    def test_null_yields_0_0 (self):
        assert_that(get_oclc_counts_from_json(None),
                    is_(equal_to((0, 0))))

    def test_empty_str_yields_0_0 (self):
        assert_that(get_oclc_counts_from_json(""),
                    is_(equal_to((0, 0))))

    def test_invalid_json_yields_0_0 (self):
        assert_that(get_oclc_counts_from_json("{{{{"),
                    is_(equal_to((0, 0))))

    def test_astro_json_yields_1_0 (self):
        assert_that(get_oclc_counts_from_json(EG_HATHI_ASTRO),
                    is_(equal_to((1, 0))))
