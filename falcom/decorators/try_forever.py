# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from time import sleep

class TryForever:

    __time_specifiers = (
        ("seconds_between_attempts", 1),
        ("minutes_between_attempts", 60),
        ("hours_between_attempts", 60*60),
    )

    def __init__ (self, kwargs):
        self.__set_properties(kwargs)
        self.__assert_no_remaining_keywords(kwargs)

    def __call__ (self, func):
        def result (*args, **kwargs):
            n = self.limit

            while True:
                try:
                    return func(*args, **kwargs)

                except:
                    n -= 1
                    if n == 0:
                        raise

                sleep(self.seconds_between_attempts)

        return result

    def __repr__ (self):
        return "<{}>".format(self.__class__.__name__)

    def __set_properties (self, kwargs):
        self.base_error = kwargs.pop("base_error", Exception)
        self.limit = kwargs.pop("limit", 0)

        self.__set_pause_time(kwargs, 60)

    def __set_pause_time (self, kwargs, default):
        all_times_given = self.__get_all_pause_times_from(kwargs)

        if all_times_given:
            self.__set_pause_time_from_list(all_times_given)

        else:
            self.seconds_between_attempts = default

    def __get_all_pause_times_from (self, kwargs):
        return [m * kwargs.pop(k)
                for k, m in self.__time_specifiers
                if k in kwargs]

    def __set_pause_time_from_list (self, all_times_given):
        self.seconds_between_attempts = all_times_given.pop(0)

        if all_times_given:
            raise TypeError("choose only one time specifier")

    def __assert_no_remaining_keywords (self, kwargs):
        if kwargs:
            key, value = kwargs.popitem()
            raise TypeError(repr(key) + " is an invalid keyword " +
                            "argument for this function")

def try_forever (*args, **kwargs):
    obj = TryForever(kwargs)

    if args:
        return obj(*args)

    else:
        return obj
