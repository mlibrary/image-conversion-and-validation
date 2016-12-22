# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import xml.etree.ElementTree as ET

class MARCData:

    def __init__ (self, xml):
        root = ET.fromstring(xml)
        self.bib = root.find(".//{http://www.loc.gov/MARC21/slim}"
                "controlfield[@tag='001']").text
        self.callno = root.find(".//{http://www.loc.gov/MARC21/slim}"
                "datafield[@tag='MDP']/{http://www.loc.gov/MARC21/slim}"
                "subfield[@code='h']").text
        author_tag = root.find(".//{http://www.loc.gov/MARC21/slim}"
                "datafield[@tag='100']/{http://www.loc.gov/MARC21/slim}"
                "subfield[@code='a']")

        if author_tag is None:
            self.author = None
        else:
            self.author = author_tag.text
