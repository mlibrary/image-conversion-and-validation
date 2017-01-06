# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
class MARCData:

    bib = None
    callno = None
    oclc = None
    author = None
    title = None
    description = None
    years = (None, None)

    def __bool__ (self):
        return False

def get_marc_data_from_xml (xml):
    if xml is not None and len(xml) > 0:
        return True

    else:
        return MARCData()
