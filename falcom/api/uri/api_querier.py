# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from time import sleep

class APIQuery:

    class __special_null: pass

    def get (self, kwargs):
        self.result = self.__special_null
        self.attempt_number = 1

        self.__try_to_get(kwargs)

        return self.result

    @staticmethod
    def utf8 (str_or_bytes):
        if isinstance(str_or_bytes, bytes):
            return str_or_bytes.decode("utf_8")

        else:
            return str_or_bytes

    def __try_to_get (self, kwargs):
        while self.result is self.__special_null:
            try:
                self.result = self.__open_uri(kwargs)

            except ConnectionError:
                self.__sleep_and_prepare_for_next_try()

    def __sleep_and_prepare_for_next_try (self):
        sleep(self.sleep_time)

        if self.attempt_number == self.max_tries:
            self.result = b""

        else:
            self.attempt_number += 1

    def __open_uri (self, kwargs):
        with self.url_opener(self.uri(**kwargs)) as response:
            result = self.utf8(response.read())

        return result

class APIQuerier:

    def __init__ (self, uri, url_opener, sleep_time=300, max_tries=0):
        self.uri = uri
        self.url_opener = url_opener
        self.sleep_time = sleep_time
        self.max_tries = max_tries

    def get (self, **kwargs):
        query = APIQuery()
        query.uri = self.uri
        query.url_opener = self.url_opener
        query.sleep_time = self.sleep_time
        query.max_tries = self.max_tries

        return query.get(kwargs)
