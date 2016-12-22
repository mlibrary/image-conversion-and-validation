# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from re import compile as re_compile
import xml.etree.ElementTree as ET

INDEX_OF_FIRST_YEAR_SUBSTR = 7
INDEX_OF_SECOND_YEAR_SUBSTR = 11
NUMBER_OF_CHARS_IN_A_YEAR = 4
MARC_NULL_YEAR = "^^^^"

# I expect OCLC text values to look like `(OCoLC)ocm15015690`. It'll
# always start with `(OCoLC)`, and I'm always only interested in the
# decimal digits at the end.
RE_MARC_OCLC = re_compile(r"^\(OCoLC\).*?([0-9]+)$")

class MARCData:

    xmlns = "http://www.loc.gov/MARC21/slim"
    description = None # should be datafield(MDP, z)

    def __init__ (self, xml):
        self.__root = ET.fromstring(xml)
        self.bib = self.__get_controlfield("001")
        self.callno = self.__get_datafield("MDP", "h")
        self.author = self.__get_datafield("100", "a")
        self.title = self.__get_datafield("245", "a")

        self.__set_years()
        self.__set_oclc()

    def __get_controlfield (self, tag):
        xpath = self.__get_control_xpath(tag)
        return self.__get_text_if_not_none(xpath)

    def __get_control_xpath (self, tag):
        return ".//{{{xmlns}}}controlfield[@tag='{}']".format(
                        tag, xmlns=self.xmlns)

    def __get_datafield (self, tag, code):
        xpath = self.__get_data_xpath(tag, code)
        return self.__get_text_if_not_none(xpath)

    def __get_data_xpath (self, tag, code):
        return ".//{{{xmlns}}}datafield[@tag='{}']/" \
                "{{{xmlns}}}subfield[@code='{}']".format(
                        tag, code, xmlns=self.xmlns)

    def __get_text_if_not_none (self, xpath):
        elt = self.__root.find(xpath)

        return getattr(elt, "text", None)

    def __find_all_datafields (self, tag, code):
        xpath = self.__get_data_xpath(tag, code)
        return self.__find_all_texts(xpath)

    def __find_all_texts (self, xpath):
        for elt in self.__root.findall(xpath):
            yield elt.text

    def __set_years (self):
        full_str = self.__get_controlfield("008")
        self.years = self.__get_first_year(full_str), \
                self.__get_second_year(full_str)

    def __get_first_year (self, full_str):
        return self.__get_year_substr(full_str,
                INDEX_OF_FIRST_YEAR_SUBSTR)

    def __get_second_year (self, full_str):
        return self.__get_year_substr(full_str,
                INDEX_OF_SECOND_YEAR_SUBSTR)

    def __get_year_substr (self, full_str, start_index):
        result = full_str[start_index:start_index +
                NUMBER_OF_CHARS_IN_A_YEAR]

        return None if result == MARC_NULL_YEAR else result

    def __set_oclc (self):
        self.oclc = self.__get_oclc()

    def __get_oclc (self):
        for value in self.__find_all_datafields("035", "a"):
            match = RE_MARC_OCLC.match(value)

            if match is not None:
                return match.group(1)

        return None
