# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import re
import xml.etree.ElementTree as ET

from .marcdata import MARCData

class ParseMarcXml:

    xmlns = "http://www.loc.gov/MARC21/slim"

    def __call__ (self, xml):
        if xml is None:
            return MARCData()

        if not isinstance(xml, ET.Element):
            try:
                xml = ET.fromstring(xml)

            except ET.ParseError:
                return MARCData()

        marc = { }
        self.xml = xml

        marc["bib"] = self.__controlfield("001")

        marc["callno"] = self.__text_or_null(
                self.xml.find(".//{{{xmlns}}}datafield[@tag='MDP']/" \
                         "{{{xmlns}}}subfield[@code='h']".format(
                                xmlns=self.xmlns)))

        marc["title"] = self.__text_or_null(
                self.xml.find(".//{{{xmlns}}}datafield[@tag='245']/" \
                         "{{{xmlns}}}subfield[@code='a']".format(
                                xmlns=self.xmlns)))

        oclcs = self.xml.findall(".//{{{xmlns}}}datafield[@tag='035']/" \
                         "{{{xmlns}}}subfield[@code='a']".format(
                                xmlns=self.xmlns))

        for maybe in oclcs:
            match = re.match(r"^\(OCoLC\).*?([0-9]+)$", maybe.text)
            if match:
                marc["oclc"] = match.group(1)
                break

        years = self.__controlfield("008")

        if years is not None:
            year1, year2 = years[7:11], years[11:15]
            if year1 == "^^^^": year1 = None
            if year2 == "^^^^": year2 = None
            marc["years"] = (year1, year2)

        return MARCData(**marc)

    def __controlfield (self, tag):
        return self.__text_or_null(
                self.xml.find(".//{{{}}}controlfield[@tag='{}']".format(
                        self.xmlns, tag)))

    def __text_or_null (self, obj):
        return getattr(obj, "text", None)

get_marc_data_from_xml = ParseMarcXml()
