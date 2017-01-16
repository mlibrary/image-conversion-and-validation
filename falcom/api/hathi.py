# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import json

class HathiItems:

    def __init__ (self):
        pass

    def __len__ (self):
        return 0

    def __iter__ (self):
        return iter(())

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

def get_hathi_data_from_json (json_data = ""):
    return HathiItems()
