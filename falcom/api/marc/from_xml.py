# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from re import compile as re_compile

from .data import MARCData
from .mapping import MARCMapping

RE_OCLC = re_compile(r"^\(OCoLC\).*?([0-9]+)$")

class MARCXMLData:

    easy_data = (
        ("bib",         ("001",)),
        ("title",       (("245", "a"),)),
        ("callno",      (("MDP", "h"),)),
        ("description", (("MDP", "z"),)),
        ("author",      (("100", "a"),)),
        ("author",      (("110", "a"), ("110", "b"))),
        ("author",      (("111", "a"),)),
        ("author",      (("130", "a"),)),
    )

    def __init__ (self, xml):
        self.marc = MARCMapping(xml)

    def get_marc_data (self):
        self.fill_in_data()
        return MARCData(**self.data)

    def fill_in_data (self):
        self.data = { }

        self.fill_in_easy_data()
        self.fill_in_oclc()
        self.fill_in_years()

    def fill_in_easy_data (self):
        for name, addresses in self.easy_data:
            self.add_value_if_we_dont_have_it(name, addresses)

    def add_value_if_we_dont_have_it (self, name, addresses):
        if name not in self.data:
            self.try_to_get_addresses(name, addresses)

    def try_to_get_addresses (self, name, addresses):
        try:
            self.data[name] = self.get_all_values(addresses)

        except StopIteration:
            pass

    def get_all_values (self, addresses):
        values = [ ]
        for address in addresses:
            values.append(next(self.marc[address]))

        return " ".join(values)

    def fill_in_oclc (self):
        for x in self.marc["035", "a"]:
            match = RE_OCLC.match(x)

            if match:
                self.data["oclc"] = "{:>09}".format(match.group(1))
                break

    def fill_in_years (self):
        try:
            long_year_str = next(self.marc["008"])

            self.data["years"] = tuple(self.extract_year(
                            long_year_str, x) for x in (7, 11))

        except StopIteration:
            pass

    def extract_year (self, long_year_str, i):
        result = long_year_str[i:i+4]

        if result != "^^^^":
            return result

def get_marc_data_from_xml (xml):
    data = MARCXMLData(xml)
    return data.get_marc_data()
