# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
class MARCData:

    callno = "Isl. Ms. 402"

    def __init__ (self, xml):
        marker = '<controlfield tag="001">'
        i = xml.index(marker) + len(marker)
        self.bib = xml[i:xml.index("<", i)]
