# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import xml.etree.ElementTree as ET

class MARCMapping:

    xmlns = "http://www.loc.gov/MARC21/slim"

    def __init__ (self, xml_str):
        if isinstance(xml_str, ET.Element):
            self.xml = xml_str

        else:
            try:
                self.xml = ET.fromstring(xml_str)

            except:
                self.xml = ET.fromstring("<empty/>")

    def __getitem__ (self, key):
        if self.__this_key_is_for_a_datafield(key):
            return self.__datafield(*key)

        else:
            return self.__controlfield(key)

    def __this_key_is_for_a_datafield (self, key):
        return isinstance(key, tuple)

    def __datafield (self, tag, code):
        paths = ("./",
                 self.__make_xpath("datafield", "tag", tag),
                 self.__make_xpath("subfield", "code", code))

        return self.__find_all("/".join(paths))

    def __controlfield (self, tag):
        xpath = ".//" + self.__make_xpath("controlfield", "tag", tag)

        return self.__find_all(xpath)

    def __make_xpath (self, field, attr, value):
        return "{{{}}}{}[@{}='{}']".format(
                self.xmlns, field, attr, value)

    def __find_all (self, xpath):
        return (elt.text for elt in self.xml.findall(xpath))
