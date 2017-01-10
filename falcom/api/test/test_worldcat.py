# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import os
import unittest

from .hamcrest import ComposedAssertion, \
        evaluates_to_false, evaluates_to_true
from ..worldcat import *

FILE_BASE = os.path.join(os.path.dirname(__file__), "files")

def readfile (filename):
    with open(os.path.join(FILE_BASE, filename), "r") as f:
        result = f.read()

    return result

EG_OCLC_ASTRO = readfile("worldcat-706055947.json")
EG_OCLC_BUSINESS = readfile("worldcat-756167029.json")
EG_OCLC_MIDAILY = readfile("worldcat-009651208.json")

class yields_empty_worldcat_data (ComposedAssertion):

    def assertion (self, item):
        data = get_worldcat_data_from_json(item)

        yield data, evaluates_to_false()
        yield list(data), is_(equal_to([]))
        yield data.title, is_(none()), "title"

class yields_worldcat_data (ComposedAssertion):

    def __init__ (self, title, libraries):
        self.title = title
        self.libraries = libraries

    def assertion (self, item):
        data = get_worldcat_data_from_json(item)

        yield data,         evaluates_to_true()
        yield data.title,   is_(equal_to(self.title)),      "title"
        yield list(data),   is_(equal_to(self.libraries))

class WorldcatDataTest (unittest.TestCase):

    def test_null_yields_empty_data (self):
        assert_that(None, yields_empty_worldcat_data())

    def test_empty_str_yields_empty_data (self):
        assert_that("", yields_empty_worldcat_data())

    def test_invalid_json_yields_empty_data (self):
        assert_that("{{{", yields_empty_worldcat_data())

    def test_astro_has_particular_data (self):
        assert_that(EG_OCLC_ASTRO, yields_worldcat_data(
                "Astronomical tables", ["EYM"]))

    def test_business_has_particular_data (self):
        assert_that(EG_OCLC_BUSINESS, yields_worldcat_data(
                "Entrepreneurial president : Richard Atkinson and"
                        " the University of California, 1995-2003",
                ["EWV", "EYM", "EYL", "EYW", "EES", "EEM", "EEI",
                 "ITS", "R2A", "EZC", "ITC", "IMX", "FW8", "CWR",
                 "CHS", "IME", "EXS", "IGR", "IHH", "IMN", "AKR",
                 "ITU", "OH1", "INA", "IEC", "AVL", "WFN", "IGB",
                 "CGU", "JAX", "INU", "IAL", "IAY", "GZC", "IIB",
                 "IMI", "III", "WMO", "H9Z", "IWC", "IFC", "DUQ",
                 "REC", "UTO", "CNTCS", "IDU", "PWA", "IUL", "PZI",
                 "IHC"]))

    def test_midaily_has_particular_data (self):
        assert_that(EG_OCLC_MIDAILY, yields_worldcat_data(
                "The Michigan daily.",
                ["HATHI", "EYM", "BEU", "EYL", "ERR", "EYW", "EEM",
                 "EUQ", "EEX", "BGU", "EXK", "EXC", "EXQ", "HV6",
                 "EXH", "UWO", "IND", "I3U", "EXN", "WOO", "EZU",
                 "OTC", "OSU", "IU0", "CDC", "IVU", "IEH", "CRL",
                 "CGU", "IBZ", "IAY", "IAA", "ICS", "IHT", "IUP",
                 "OUN", "ICG", "ICX", "PQA", "WEZ", "IUL", "JYJ",
                 "EZL", "EZB", "GZM", "YGM", "VQT", "RVE", "UPM",
                 "IDB"]))
