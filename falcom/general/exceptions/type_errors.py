# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

from ..counted_word import CountedWord

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

class MultipleValuesOneArgError (TypeError):

    def __new__ (cls, function_name, arg):
        return TypeError(
                "{}() got multiple values for keyword argument '{}'"
                        .format(function_name, arg))

class TooManyArgumentsError (TypeError):

    def __new__ (cls, function_name, expected, received):
        args = CountedWord("positional argument")
        were = CountedWord("was", "were")

        return TypeError("{}() takes {} but {} given".format(
                function_name, args(expected), were(received)))
