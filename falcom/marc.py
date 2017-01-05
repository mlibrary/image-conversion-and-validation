# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
class MARCData:

    bib = None

    def __bool__ (self):
        return False

def get_marc_data_from_xml (xml):
    return MARCData()
