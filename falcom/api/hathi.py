# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import json

from .common.read_only_data_structure import ReadOnlyDataStructure

class HathiData (ReadOnlyDataStructure):

    @property
    def titles (self):
        return self.get("titles", ())

    @property
    def htids (self):
        return self.get("htids", ())

def get_counts_from_item_list (items, htid):
    a = len([x for x in items if x["htid"] == htid])
    b = len(items) - a

    return a, b

def get_oclc_counts_from_json (json_data, htid = ""):
    try:
        data = json.loads(json_data)
        return get_counts_from_item_list(data["items"], htid)

    except:
        return 0, 0

def load_json (json_data, default):
    try:
        return json.loads(json_data)

    except:
        return default

def get_titles_from_data (data):
    result = [ ]
    for x in data.get("records", { }).values():
        result.extend(x.get("titles", ()))

    return result if result else None

def get_hathi_data_from_json (json_data = ""):
    data = load_json(json_data, { })
    return HathiData(titles=get_titles_from_data(data))
