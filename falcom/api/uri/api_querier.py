# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class APIQuerier:

    def __init__ (self, uri, url_opener):
        self.uri = uri
        self.url_opener = url_opener

    def get (self, **kwargs):
        response = self.url_opener(self.uri(**kwargs))
        response.read()
        response.read()
        response.read()
