# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from json import loads as json_load

from .data import WorldcatData

def get_worldcat_data_from_json (json_data):
    try:
        data = json_load(json_data)
        return WorldcatData(title=data["title"],
                            libraries=[l["oclcSymbol"]
                                        for l in data["library"]])

    except:
        return WorldcatData()
