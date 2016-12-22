# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import xml.etree.ElementTree as ET

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

    def __get_controlfield (self, tag):
        return self.__get_text_if_not_none(
                ".//{{{xmlns}}}controlfield[@tag='{}']".format(
                        tag, xmlns=self.xmlns))

    def __get_datafield (self, tag, code):
        return self.__get_text_if_not_none(
                ".//{{{xmlns}}}datafield[@tag='{}']/"
                "{{{xmlns}}}subfield[@code='{}']".format(
                        tag, code, xmlns=self.xmlns))

    def __get_text_if_not_none (self, xpath):
        elt = self.__root.find(xpath)

        return getattr(elt, "text", None)

    def __set_years (self):
        full_008_str = self.__get_controlfield("008")
        year1 = self.__get_year_substr(full_008_str, 7)
        year2 = self.__get_year_substr(full_008_str, 11)

        self.years = year1, year2

    def __get_year_substr (self, full_008_str, start_index):
        result = full_008_str[start_index:start_index+4]

        return None if result == "^^^^" else result
