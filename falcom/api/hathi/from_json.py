# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from json import loads as json_load_str

from .data import HathiData

class HathiJsonData:

    def __init__ (self, json_data):
        self.__load_json(json_data)

    def get_hathi_data (self):
        return HathiData(titles=self.__get_titles_from_data(),
                         htids=self.__get_htids_from_data())

    def __load_json (self, json_data):
        try:
            self.data = json_load_str(json_data)

        except:
            self.__set_to_empty_json_data()

    def __set_to_empty_json_data (self):
        self.data = { }

    def __get_titles_from_data (self):
        result = [ ]
        for title_list in self.__title_lists_in_data():
            result.extend(title_list)

        return self.__get_None_if_empty(result)

    def __title_lists_in_data (self):
        return (x.get("titles", ()) for x in self.data.get("records", {}).values())

    def __get_htids_from_data (self):
        return self.__get_None_if_empty(self.__htids_in_data(self.data))

    def __htids_in_data (self, data):
        return [x["htid"] for x in data.get("items", []) if "htid" in x]

    def __get_None_if_empty (self, container):
        return container if container else None

def get_hathi_data_from_json (json_data = ""):
    data = HathiJsonData(json_data)
    return data.get_hathi_data()
