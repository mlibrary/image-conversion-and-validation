# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
def get_marc_data_from_xml (xml):
    return {
            "bib": None,
            "callno": None,
            "oclc": None,
            "author": None,
            "title": None,
            "description": None,
            "years": (None, None),
    }
