# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from time import sleep

class APIQuery:

    def get (self, kwargs):
        self.kwargs = kwargs

        if self.max_tries > 0:
            return self.__get_with_max()

        else:
            return self.__get_forever()

    def __get_forever (self):
        while True:
            try:
                return self.__open_uri()

            except ConnectionError:
                self.__sleep()

    def __get_with_max (self):
        n = 0
        while n < self.max_tries:
            try:
                return self.__open_uri()

            except ConnectionError:
                self.__sleep()
                n += 1

        return ""

    def __sleep (self):
        sleep(self.sleep_time)

    @staticmethod
    def utf8 (str_or_bytes):
        if isinstance(str_or_bytes, bytes):
            return str_or_bytes.decode("utf_8")

        else:
            return str_or_bytes

    def __open_uri (self):
        with self.url_opener(self.uri(**self.kwargs)) as response:
            result = self.utf8(response.read())

        return result

class APIQuerier:

    def __init__ (self, uri, url_opener, sleep_time=300, max_tries=0):
        self.uri = uri
        self.url_opener = url_opener
        self.sleep_time = sleep_time
        self.max_tries = max_tries

    def get (self, **kwargs):
        return self.__new_query().get(kwargs)

    def __new_query (self):
        query = APIQuery()
        self.__copy_self_to_query(query)
        return query

    def __copy_self_to_query (self, query):
        query.uri = self.uri
        query.url_opener = self.url_opener
        query.sleep_time = self.sleep_time
        query.max_tries = self.max_tries
