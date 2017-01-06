# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import re
import xml.etree.ElementTree as ET

from .marcdata import MARCData

class ParseMarcXml:

    xmlns = "http://www.loc.gov/MARC21/slim"

    def __call__ (self, xml):
        self.xml = xml

        return self.__get_marc_data_if_we_have_xml()

    def __get_marc_data_if_we_have_xml (self):
        if self.__xml_is_empty():
            return MARCData()

        else:
            return self.__extract_xml()

    def __xml_is_empty (self):
        if self.xml is None:
            return True

        else:
            return self.__we_dont_have_xml()

    def __we_dont_have_xml (self):
        if isinstance(self.xml, ET.Element):
            return False

        else:
            return self.__cant_parse_xml()

    def __cant_parse_xml (self):
        try:
            self.xml = ET.fromstring(self.xml)

        except ET.ParseError:
            return True

    def __extract_xml (self):
        marc = { }
        marc["bib"] = self.__controlfield("001")
        marc["callno"] = self.__datafield("MDP", "h")
        marc["title"] = self.__datafield("245", "a")
        marc["oclc"] = self.__get_oclc()
        marc["years"] = self.__get_years()

        return MARCData(**marc)

    def __get_years (self):
        years = self.__controlfield("008")

        if years is not None:
            year1, year2 = years[7:11], years[11:15]
            if year1 == "^^^^": year1 = None
            if year2 == "^^^^": year2 = None
            return year1, year2

    def __get_oclc (self):
        oclcs = self.xml.findall(".//{{{xmlns}}}datafield[@tag='035']/" \
                         "{{{xmlns}}}subfield[@code='a']".format(
                                xmlns=self.xmlns))

        for maybe in oclcs:
            match = re.match(r"^\(OCoLC\).*?([0-9]+)$", maybe.text)
            if match:
                return match.group(1)

    def __datafield (self, tag, code):
        return self.__text_or_null(
                self.xml.find(".//{{{xmlns}}}datafield[@tag='{}']/" \
                        "{{{xmlns}}}subfield[@code='{}']".format(
                                tag, code, xmlns=self.xmlns)))

    def __controlfield (self, tag):
        return self.__text_or_null(
                self.xml.find(".//{{{}}}controlfield[@tag='{}']".format(
                        self.xmlns, tag)))

    def __text_or_null (self, obj):
        return getattr(obj, "text", None)

get_marc_data_from_xml = ParseMarcXml()
