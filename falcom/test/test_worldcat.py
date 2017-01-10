# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import os
import unittest

from ..worldcat import *

FILE_BASE = os.path.join(os.path.dirname(__file__), "files")

def readfile (filename):
    with open(os.path.join(FILE_BASE, filename), "r") as f:
        result = f.read()

    return result

EG_OCLC_ASTRO = readfile("worldcat-706055947.json")
EG_OCLC_BUSINESS = readfile("worldcat-756167029.json")
EG_OCLC_MIDAILY = readfile("worldcat-009651208.json")

class WorldcatDataTest (unittest.TestCase):

    def test_nothing (self):
        data = get_worldcat_data_from_json(None)