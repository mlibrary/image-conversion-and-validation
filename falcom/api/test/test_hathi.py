# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import os
import unittest

from .hamcrest import ComposedAssertion, \
        evaluates_to_false, evaluates_to_true

FILE_BASE = os.path.join(os.path.dirname(__file__), "files")

def readfile (filename):
    with open(os.path.join(FILE_BASE, filename), "r") as f:
        result = f.read()

    return result

EG_HATHI_ASTRO = readfile("hathitrust-706055947.json")
EG_HATHI_BUSINESS = readfile("hathitrust-756167029.json")
EG_HATHI_MIDAILY = readfile("hathitrust-009651208.json")

class NothingTest (unittest.TestCase):

    def test_exists (self):
        pass
