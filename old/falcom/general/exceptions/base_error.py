# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from re import compile as re_compile

RE_INDENT = re_compile(r"\n +")

class BaseError (RuntimeError):
    """Catchall exception to sire all others in this script.

    The idea here is that the docstring of any child exceptions will be
    used as the message string. Also, it'll ignore everything after the
    first paragraph (i.e. anything after a double-newline).

    So, if you implement this exception directly, its message should
    simply be:

        Catchall exception to sire all others in this script.

    If you want to format the message string, you can pass args at init,
    and the'll be passed to the docstring with a str.format() call.

    I don't do anything for keyword arguments. I'm not trying to make
    this complicated.
    """

    def __init__ (self, *args):
        """Set the internal message and value."""

        if args:
            self.__parse_args_and_set_values(args)

        else:
            self.__set_default_values()

    def __str__ (self):
        """Return the str message."""
        return self.message

    def __set_default_values (self):
        self.message = self.__get_summary()
        self.value = None

    def __parse_args_and_set_values (self, args):
        summary = self.__get_summary()
        self.message = summary.format(*args)
        self.__set_value(args)

    def __get_summary (self):
        docstr_without_indents = RE_INDENT.sub("\n", self.__doc__)
        first_paragraph = self.__strip_double_newline(
                docstr_without_indents)
        return first_paragraph.replace("\n", " ")

    def __strip_double_newline (self, text):
        i = text.find("\n\n")

        return text if i == -1 else text[:i]

    def __set_value (self, args):
        if len(args) == 1:
            self.value = args[0]

        else:
            self.value = args
