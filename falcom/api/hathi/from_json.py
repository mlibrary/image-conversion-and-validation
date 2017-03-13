# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import json

from .data import HathiData

def load_json (json_data):
    try:
        return json.loads(json_data)

    except:
        return { }

def get_None_if_empty (container):
    return container if container else None

def title_lists_in_data (data):
    return (x.get("titles", ()) for x in data.get("records", {}).values())

def get_titles_from_data (data):
    result = [ ]
    for title_list in title_lists_in_data(data):
        result.extend(title_list)

    return get_None_if_empty(result)

def htids_in_data (data):
    return [x["htid"] for x in data.get("items", []) if "htid" in x]

def get_htids_from_data (data):
    return get_None_if_empty(htids_in_data(data))

def get_hathi_data_from_json (json_data = ""):
    data = load_json(json_data)
    return HathiData(titles=get_titles_from_data(data),
                     htids=get_htids_from_data(data))
