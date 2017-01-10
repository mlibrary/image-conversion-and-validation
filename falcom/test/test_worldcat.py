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

class is_empty_worldcat_data (ComposedAssertion):

    def assertion (self, item):
        yield evaluates_to_false()
        yield list(item), is_(equal_to([]))
        yield item.title, is_(none()), "title"

class WorldcatDataTest (unittest.TestCase):

    def test_null_yields_empty_data (self):
        data = get_worldcat_data_from_json(None)
        assert_that(data, is_empty_worldcat_data())

    def test_empty_str_yields_empty_data (self):
        data = get_worldcat_data_from_json("")
        assert_that(data, is_empty_worldcat_data())

    def test_astro_has_title (self):
        data = get_worldcat_data_from_json(EG_OCLC_ASTRO)
        assert_that(data.title, is_(equal_to("Astronomical tables")))
        assert_that(data, evaluates_to_true())
        assert_that(list(data), is_(equal_to(["EYM"])))
