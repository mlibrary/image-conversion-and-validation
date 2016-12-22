# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import unittest

from .counted_word import CountedWord

class TestCountedWord (unittest.TestCase):

    def init_counted_word (self, *args):
        self.word = CountedWord(*args)

    def assert_getstr (self, number, rhs):
        self.assertEqual(self.word(number), rhs)

    def test_different_simple_nouns (self):
        self.init_counted_word("thing")
        self.assert_getstr(0, "0 things")
        self.assert_getstr(1, "1 thing")
        self.assert_getstr(2, "2 things")

        self.init_counted_word("widget")
        self.assert_getstr(0, "0 widgets")
        self.assert_getstr(1, "1 widget")
        self.assert_getstr(2, "2 widgets")

    def test_custom_plural (self):
        self.init_counted_word("octopus", "octopodes")
        self.assert_getstr(0, "0 octopodes")
        self.assert_getstr(1, "1 octopus")
        self.assert_getstr(2, "2 octopodes")

    def test_repr (self):
        self.init_counted_word("beat")
        self.assertEqual(repr(self.word), "<CountedWord beat/beats>")

        self.init_counted_word("holler")
        self.assertEqual(repr(self.word),
                         "<CountedWord holler/hollers>")

        self.init_counted_word("forum", "fora")
        self.assertEqual(repr(self.word), "<CountedWord forum/fora>")

    def test_repr_on_child_class (self):
        class SomeDerivativeOfCountedWord (CountedWord):
            pass

        w = SomeDerivativeOfCountedWord("rock")
        self.assertEqual(repr(w),
                         "<SomeDerivativeOfCountedWord rock/rocks>")
