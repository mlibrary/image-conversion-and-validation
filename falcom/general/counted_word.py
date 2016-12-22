# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

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

        return "<{} {}/{}>".format(self.__class__.__name__,
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
