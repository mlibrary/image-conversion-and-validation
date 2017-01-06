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
        return MARCData(bib=self.__find_controlfield("001"),
                        callno=self.__find_datafield("MDP", "h"),
                        author=self.__find_datafield("100", "a"),
                        title=self.__find_datafield("245", "a"),
                        oclc=self.__get_oclc(),
                        years=self.__get_years())

    def __get_years (self):
        long_year_str = self.__find_controlfield("008")

        if long_year_str:
            return tuple(self.__extract_year(long_year_str, x)
                    for x in (7, 11))

    def __extract_year (self, long_year_str, i):
        result = long_year_str[i:i+4]

        if result != "^^^^":
            return result

    def __get_oclc (self):
        for oclc in self.__iterate_through_valid_oclcs():
            return oclc

    def __iterate_through_valid_oclcs (self):
        return (m.group(1)
                for m in self.__iterate_through_oclc_matches()
                if m)

    def __iterate_through_oclc_matches (self):
        return (RE_OCLC.match(e.text)
                for e in self.__get_all_oclc_elts())

    def __get_all_oclc_elts (self):
        return self.xml.findall(self.__datafiend_xpath("035", "a"))

    def __find_datafield (self, tag, code):
        return self.__text_or_null(self.xml.find(
                self.__datafiend_xpath(tag, code)))

    def __find_controlfield (self, tag):
        return self.__text_or_null(self.xml.find(
                self.__controlfiend_xpath(tag)))

    def __datafiend_xpath (self, tag, code):
        return self.__generate_xpath(("datafield", "tag", tag),
                                     ("subfield", "code", code))

    def __controlfiend_xpath (self, tag):
        return self.__generate_xpath(("controlfield", "tag", tag))

    def __generate_xpath (self, *triples):
        return ".//" + "/".join(
                "{{{}}}{}[@{}='{}']".format(
                        self.xmlns, field, attr, value)
                for field, attr, value in triples)

    def __text_or_null (self, obj):
        return getattr(obj, "text", None)

get_marc_data_from_xml = ParseMarcXml()
