# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from ...decorators import try_forever

class APIQuery:

    def get (self, kwargs):
        self.kwargs = kwargs
        try_to_get_data = self.__get_forever_looper()

        try:
            return try_to_get_data()

        except ConnectionError:
            return ""

    def __get_forever_looper (self):
        decorator = try_forever(
                seconds_between_attempts=self.sleep_time,
                base_error=ConnectionError,
                limit=self.max_tries)

        return decorator(self.__open_uri)

    def __get_forever (self):
        while True:
            try:
                return self.__open_uri()

            except ConnectionError:
                self.__pause_between_attempts()

    def __get_with_max (self):
        n = 0
        while n < self.max_tries:
            try:
                return self.__open_uri()

            except ConnectionError:
                self.__pause_between_attempts()
                n += 1

        return ""

    def __pause_between_attempts (self):
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
