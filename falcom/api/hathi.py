# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import json

def get_counts_from_item_list (items, barcode):
    a = 0
    b = 0

    for item in items:
        if item["htid"] == "mdp." + barcode:
            a += 1

        else:
            b += 1

    return a, b

def get_oclc_counts_from_json (json_data, barcode = ""):
    try:
        data = json.loads(json_data)
        return get_counts_from_item_list(data["items"], barcode)

    except:
        return 0, 0
