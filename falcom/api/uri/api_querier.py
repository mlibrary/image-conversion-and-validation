# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class APIQuerier:

    def __init__ (self, uri, url_opener):
        self.uri = uri
        self.url_opener = url_opener

    def get (self, **kwargs):
        with self.url_opener(self.uri(**kwargs)) as response:
            result = self.utf8(response.read())

        return result

    @staticmethod
    def utf8 (str_or_bytes):
        if isinstance(str_or_bytes, bytes):
            return str_or_bytes.decode("utf_8")

        else:
            return str_or_bytes
