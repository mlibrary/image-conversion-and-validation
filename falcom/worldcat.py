# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import json

class WorldcatData:

    @property
    def title (self):
        return self.__wc_dict.get("title", None)

    @property
    def libraries (self):
        return self.__wc_dict.get("libraries", ())

    def __init__ (self, **kwargs):
        self.__wc_dict = kwargs
        null_keys = [k for k, v in kwargs.items() if v is None]
        for key in null_keys:
            del kwargs[key]

    def __bool__ (self):
        return False

def get_worldcat_data_from_json (json_data):
    try:
        data = json.loads(json_data)
        return WorldcatData(title=data["title"])

    except TypeError:
        return WorldcatData()
