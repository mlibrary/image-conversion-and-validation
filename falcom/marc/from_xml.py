# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from re import compile as re_compile
import xml.etree.ElementTree as ET

from .marcdata import MARCData

RE_OCLC = re_compile(r"^\(OCoLC\).*?([0-9]+)$")

class ParseMarcXml:

    xmlns = "http://www.loc.gov/MARC21/slim"

    def __call__ (self, xml):
        self.xml = xml

        return self.__get_marc_data_if_we_have_xml()

    def __get_marc_data_if_we_have_xml (self):
        if self.__we_have_xml():
            return self.__extract_xml()

        else:
            return MARCData()

    def __we_have_xml (self):
        if self.xml is None:
            return False

        else:
            return self.__we_have_an_etree()

    def __we_have_an_etree (self):
        if isinstance(self.xml, ET.Element):
            return True

        else:
            return self.__we_can_parse_xml()

    def __we_can_parse_xml (self):
        try:
            return self.__parse_the_xml_str()

        except ET.ParseError:
            return False

    def __parse_the_xml_str (self):
        self.xml = ET.fromstring(self.xml)
        return True

    def __extract_xml (self):
        return MARCData(bib=self.__controlfield("001"),
                        callno=self.__datafield("MDP", "h"),
                        title=self.__datafield("245", "a"),
                        oclc=self.__get_oclc(),
                        years=self.__get_years())

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
            match = RE_OCLC.match(maybe.text)
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
