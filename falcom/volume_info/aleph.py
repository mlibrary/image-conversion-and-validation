# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import xml.etree.ElementTree as ET

class MARCData:

    author = ""

    def __init__ (self, xml):
        root = ET.fromstring(xml)
        self.bib = root.find(".//{http://www.loc.gov/MARC21/slim}"
                "controlfield[@tag='001']").text
        self.callno = root.find(".//{http://www.loc.gov/MARC21/slim}"
                "datafield[@tag='MDP']/{http://www.loc.gov/MARC21/slim}"
                "subfield[@code='h']").text
