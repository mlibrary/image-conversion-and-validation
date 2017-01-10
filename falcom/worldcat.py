# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import json

from .common import ReadOnlyDataStructure

class WorldcatData (ReadOnlyDataStructure):

    @property
    def title (self):
        return self.get("title")

    def __iter__ (self):
        return iter(self.get("libraries", ()))

def get_worldcat_data_from_json (json_data):
    try:
        data = json.loads(json_data)
        return WorldcatData(title=data["title"],
                            libraries=[l["oclcSymbol"]
                                        for l in data["library"]])

    except:
        return WorldcatData()
