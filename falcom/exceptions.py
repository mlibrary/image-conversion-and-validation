# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from re import compile as re_compile

class BaseError (Exception):
    """Catchall exception to sire all others in this script."""

    __re_indent = re_compile(r"\n +")

    def __init__ (self, *args):
        """Set the internal message and value."""

        if len(args) == 0:
            # If there aren't any args, then we want default values.
            self.__default_values()

        else:
            # If there are any args, then we'll want to format the
            # message based on them.
            self.message = self.__prep_docstr().format(*args)

            # The value will depend on the number of args.
            self.__set_value(args)

    def __str__ (self):
        """Return the str message."""
        return self.message

    def __prep_docstr (self):
        # First, we strip away any indentations so that each line begins
        # with no leading whitespace.
        no_indents = self.__re_indent.sub("\n", self.__doc__)

        # Second, we look for a double newline, and strip it away along
        # with anything following it. This way, we ignore any paragraphs
        # following the summary that we actually want to use.
        relevant_piece = self.__strip_double_newline(no_indents)

        # Finally, we separate lines by spaces instead of newlines.
        return relevant_piece.replace("\n", " ")

    def __strip_double_newline (self, text):
        # Find a double-newline.
        i = text.find("\n\n")

        if i == -1:
            # Couldn't find one. That means we use the entire text.
            return text

        else:
            # Found one! Use everything leading up to the first double
            # newline.
            return text[:i]

    def __default_values (self):
        # By default, we just use the docstring with a null value.
        self.message = self.__prep_docstr()
        self.value = None

    def __set_value (self, args):
        if len(args) == 1:
            # If there's a single argument, then we can just use it.
            self.value = args[0]

        else:
            # If there's more than one, then we should use the entire
            # tuple as the value.
            self.value = args

class InputFileError (BaseError):
    """Generic input file error."""
    pass

class CantDecodeEncoding (InputFileError):
    """Can't figure out file encoding for {}"""
    pass

class InvalidControls (CantDecodeEncoding):
    """Unexpected control character (0x{:02x}) in {}"""
    pass

class InconsistentNewlines (InputFileError):
    """Some combination of LF, CR, and CRLFs in {}"""
    pass

class InconsistentColumnCounts (InputFileError):
    """Expected each row to have the same column count in {}"""
    pass

class CountedWord:
    """A word prepared to enter sentences accompanied by a quantity."""

    def __init__ (self, singular_word, optional_plural = None):
        """Init internal parameters.

        If you don't give me an optional plural, I'll default to
        appending an `s` to the end of the singular word.
        """

        self.__singular = singular_word
        self.__figure_out_plural(optional_plural)

    def __call__ (self, quantity):
        """Return a string of the form `# word(s)`.

        Whether we return the singular or the plural form of the word
        depends on whether or not the quantity is 1.
        """

        if quantity == 1:
            return self.__get_singular()

        else:
            return self.__get_plural(quantity)

    def __repr__ (self):
        """Return informataive representation of CountedWord object."""

        return "<{} {}/{}>".format(
                self.__class__.__name__,
                self.__singular,
                self.__plural)

    def __figure_out_plural (self, optional_plural):
        if optional_plural is None:
            self.__set_default_plural()

        else:
            self.__set_specific_plural(optional_plural)

    def __set_default_plural (self):
        self.__plural = self.__singular + "s"

    def __set_specific_plural (self, plural):
        self.__plural = plural

    def __get_singular (self):
        return "1 " + self.__singular

    def __get_plural (self, quantity):
        return "{:d} {}".format(quantity, self.__plural)

class TooManyArgumentsError (TypeError):

    def __new__ (cls, function_name, expected, received):
        args = CountedWord("positional argument")
        were = CountedWord("was", "were")

        return TypeError("{}() takes {} but {} given".format(
                function_name, args(expected), were(received)))

class MultipleValuesOneArgError (TypeError):

    def __new__ (cls, function_name, arg):
        return TypeError(
                "{}() got multiple values for keyword argument '{}'"
                        .format(function_name, arg))

class MissingPositionalArgsError (TypeError):

    def __new__ (cls, function_name, *args):
        missing = CountedWord("required positional argument")
        list_str = cls.__get_english_str_of_list(args)

        return TypeError("{}() missing {}: {}".format(
                function_name, missing(len(args)), list_str))

    @classmethod
    def __get_english_str_of_list (cls, sequence):
        if len(sequence) > 2:
            return cls.__get_str_of_list_of_3_or_more(sequence)

        else:
            return cls.__get_str_of_list_of_2_or_fewer(sequence)

    @classmethod
    def __get_str_of_list_of_3_or_more (cls, sequence):
        l = cls.__get_list_of_reprs_of_each_elt(sequence)
        cls.__prepend_and_to_last_elt(l)
        return ", ".join(l)

    @staticmethod
    def __get_list_of_reprs_of_each_elt (iterable):
        return list(map(repr, iterable))

    @staticmethod
    def __prepend_and_to_last_elt (list_of_elts):
        list_of_elts.append("and " + list_of_elts.pop())

    @staticmethod
    def __get_str_of_list_of_2_or_fewer (sequence):
        return " and ".join(map(repr, sequence))
