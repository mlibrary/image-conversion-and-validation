# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from time import sleep

class APIQuerier:

    def __init__ (self, uri, url_opener, sleep_time=300, max_tries=0):
        self.uri = uri
        self.url_opener = url_opener
        self.sleep_time = sleep_time
        self.max_tries = max_tries

    def get (self, **kwargs):
        try:
            return self.__open_uri(kwargs)

        except ConnectionError:
            sleep(self.sleep_time)

        i = 1
        while i != self.max_tries:
            i += 1

            try:
                return self.__open_uri(kwargs)

            except ConnectionError:
                sleep(self.sleep_time)

        return b""

    @staticmethod
    def utf8 (str_or_bytes):
        if isinstance(str_or_bytes, bytes):
            return str_or_bytes.decode("utf_8")

        else:
            return str_or_bytes

    def __open_uri (self, kwargs):
        with self.url_opener(self.uri(**kwargs)) as response:
            result = self.utf8(response.read())

        return result
