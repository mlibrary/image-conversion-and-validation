# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ...test.hamcrest import ComposedMatcher, evaluates_to
from ...test.read_example_file import ExampleFileTest
from ..worldcat import *

class yields_empty_worldcat_data (ComposedMatcher):

    def assertion (self, item):
        data = get_worldcat_data_from_json(item)

        yield data, evaluates_to(False)
        yield list(data), is_(equal_to([]))
        yield data.title, is_(none()), "title"

class yields_worldcat_data (ComposedMatcher):

    def __init__ (self, title, libraries):
        self.title = title
        self.libraries = libraries

    def assertion (self, item):
        data = get_worldcat_data_from_json(item)

        yield data,         evaluates_to(True)
        yield data.title,   is_(equal_to(self.title)),      "title"
        yield list(data),   is_(equal_to(self.libraries))

class WorldcatFileTest (ExampleFileTest):
    this__file__ = __file__
    format_str = "worldcat-{}.json"

class WorldcatDataTest (unittest.TestCase):

    def test_null_yields_empty_data (self):
        assert_that(None, yields_empty_worldcat_data())

    def test_empty_str_yields_empty_data (self):
        assert_that("", yields_empty_worldcat_data())

    def test_invalid_json_yields_empty_data (self):
        assert_that("{{{", yields_empty_worldcat_data())

class GivenAstronomyJson (WorldcatFileTest):
    filename = "706055947"

    def test_astro_has_particular_data (self):
        assert_that(self.file_data, yields_worldcat_data(
                "Astronomical tables", ["EYM"]))

class GivenBusinessJson (WorldcatFileTest):
    filename = "756167029"

    def test_business_has_particular_data (self):
        assert_that(self.file_data, yields_worldcat_data(
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

class GivenMichiganDailyJson (WorldcatFileTest):
    filename = "009651208"

    def test_midaily_has_particular_data (self):
        assert_that(self.file_data, yields_worldcat_data(
                "The Michigan daily.",
                ["HATHI", "EYM", "BEU", "EYL", "ERR", "EYW", "EEM",
                 "EUQ", "EEX", "BGU", "EXK", "EXC", "EXQ", "HV6",
                 "EXH", "UWO", "IND", "I3U", "EXN", "WOO", "EZU",
                 "OTC", "OSU", "IU0", "CDC", "IVU", "IEH", "CRL",
                 "CGU", "IBZ", "IAY", "IAA", "ICS", "IHT", "IUP",
                 "OUN", "ICG", "ICX", "PQA", "WEZ", "IUL", "JYJ",
                 "EZL", "EZB", "GZM", "YGM", "VQT", "RVE", "UPM",
                 "IDB"]))
