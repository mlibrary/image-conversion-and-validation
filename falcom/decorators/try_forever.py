# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class TryForever:

    __time_specifiers = (
        ("seconds_between_attempts", 1),
        ("minutes_between_attempts", 60),
    )

    def __init__ (self, kwargs):
        self.base_error = kwargs.pop("base_error", Exception)
        self.limit = kwargs.pop("limit", 0)

        self.__set_pause_time(kwargs, 60)

        self.__assert_no_remaining_keywords(kwargs)

    def __call__ (self, func):
        return func

    def __repr__ (self):
        return "<{}>".format(self.__class__.__name__)

    def __set_pause_time (self, kwargs, default):
        secs = [m * kwargs.pop(k)
                for k, m in self.__time_specifiers
                if k in kwargs]

        if secs:
            self.seconds_between_attempts = secs.pop(0)

            if secs:
                raise TypeError("choose only one time specifier")

        else:
            self.seconds_between_attempts = default

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
