# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

from ..common import ReadOnlyDataStructure

class MARCData (ReadOnlyDataStructure):

    auto_properties = (
        "bib",
        "callno",
        "oclc",
        "author",
        "title",
        "description",
        ("years", (None, None)),
    )
