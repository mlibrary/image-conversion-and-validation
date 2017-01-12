# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import json

def get_oclc_counts_from_json (json_data, barcode = ""):
    try:
        data = json.loads(json_data)
        return len(data["items"]), 0

    except:
        return 0, 0
