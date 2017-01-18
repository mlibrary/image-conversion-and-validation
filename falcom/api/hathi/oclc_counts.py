# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

from .from_json import get_hathi_data_from_json

def get_oclc_counts_from_json (json_data, htid = ""):
    data = get_hathi_data_from_json(json_data)
    return data.get_item_counts(htid)
