# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

from ..common import ReadOnlyDataStructure

class WorldcatData (ReadOnlyDataStructure):

    auto_properties = ("title",)

    def __iter__ (self):
        return iter(self.get("libraries", ()))
