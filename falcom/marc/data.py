# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

from ..common import ReadOnlyDataStructure

class MARCData (ReadOnlyDataStructure):

    @property
    def bib (self):
        return self.get("bib")

    @property
    def callno (self):
        return self.get("callno")

    @property
    def oclc (self):
        return self.get("oclc")

    @property
    def author (self):
        return self.get("author")

    @property
    def title (self):
        return self.get("title")

    @property
    def description (self):
        return self.get("description")

    @property
    def years (self):
        return self.get("years", (None, None))
