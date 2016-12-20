# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import unittest

from ..argument_collector import *

class TestArgumentCollector (unittest.TestCase):

    def test_zero_args (self):
        ac = ArgumentCollector()
        self.assertFalse(bool(ac))
        self.assertEqual(len(ac), 0)

        ac.update(hey = "hello")
        self.assertTrue(bool(ac))
        self.assertEqual(len(ac), 1)
        self.assertTrue("hey" in ac)
        self.assertFalse("what" in ac)

        ac.update(what = "whaddup")
        self.assertTrue(bool(ac))
        self.assertEqual(len(ac), 1)
        self.assertFalse("hey" in ac)
        self.assertTrue("what" in ac)

    def test_one_arg (self):
        ac = ArgumentCollector("matt")
        self.assertFalse(bool(ac))
        self.assertEqual(len(ac), 0)

    def test_one_arg_one_kwarg (self):
        ac = ArgumentCollector("hi", matt="is cool")
        self.assertFalse(bool(ac))
        self.assertEqual(len(ac), 1)

    def test_is_mapping (self):
        self.assertTrue(issubclass(ArgumentCollector, Mapping))

    def test_wrong_args (self):
        accepts_five = ArgumentCollector("a", "b", "c", "d", "e")

        with self.assertRaises(TypeError):
            accepts_five.update(1, 2, 3, 4)

        with self.assertRaises(TypeError):
            accepts_five.update(1, 2, 3, 4, 5, 6)

        with self.assertRaises(TypeError):
            accepts_five.update(1, 2, 3, 4, c = 5)

    def test_basic_args (self):
        accepts_five = ArgumentCollector("a", "b", "c", "d", "e")

        accepts_five.update(1, 2, 3, 4, 5)
        self.assertEqual(len(accepts_five), 5)
        self.assertEqual(accepts_five, {
                        "a": 1,
                        "b": 2,
                        "c": 3,
                        "d": 4,
                        "e": 5})

        accepts_five.update(5, 4, 3, 2, 1)
        self.assertEqual(len(accepts_five), 5)
        self.assertEqual(accepts_five, {
                        "e": 1,
                        "d": 2,
                        "c": 3,
                        "b": 4,
                        "a": 5})

        accepts_five.update(1, 2, 3, 4, 5, ok="what")
        self.assertEqual(len(accepts_five), 6)
        self.assertEqual(accepts_five, {
                        "ok": "what",
                        "a": 1,
                        "b": 2,
                        "c": 3,
                        "d": 4,
                        "e": 5})

        accepts_five.update(1, 2, 3, 4, 5)
        self.assertEqual(len(accepts_five), 5)
        self.assertEqual(accepts_five, {
                        "a": 1,
                        "b": 2,
                        "c": 3,
                        "d": 4,
                        "e": 5})

    def test_kwargs (self):
        with_defaults = ArgumentCollector("a", "b", c=1, d=2, e=3)

        with_defaults.update(1, 2)
        self.assertEqual(len(with_defaults), 5)
        self.assertEqual(with_defaults, {
                        "a": 1,
                        "b": 2,
                        "c": 1,
                        "d": 2,
                        "e": 3})

        with_defaults.update(123, 234, d=345)
        self.assertEqual(len(with_defaults), 5)
        self.assertEqual(with_defaults, {
                        "a": 123,
                        "b": 234,
                        "c": 1,
                        "d": 345,
                        "e": 3})

        with_defaults.update("hi", "hello")
        self.assertEqual(len(with_defaults), 5)
        self.assertEqual(with_defaults, {
                        "a": "hi",
                        "b": "hello",
                        "c": 1,
                        "d": 2,
                        "e": 3})

        with_defaults.update(1, 2, f="matt")
        self.assertEqual(len(with_defaults), 6)
        self.assertEqual(with_defaults, {
                        "a": 1,
                        "b": 2,
                        "c": 1,
                        "d": 2,
                        "e": 3,
                        "f": "matt"})

        with_defaults.update(1, 2)
        self.assertEqual(len(with_defaults), 5)
        self.assertEqual(with_defaults, {
                        "a": 1,
                        "b": 2,
                        "c": 1,
                        "d": 2,
                        "e": 3})

    def test_repr (self):
        eg_ac = ArgumentCollector("a", "b", hi="hello", d="hey")
        eg_ac.update(1, 2, c=3, d=4)

        start = "<ArgumentCollector {"
        end = "}>"
        length = len(start) + len(end)

        repr_str = repr(eg_ac)

        self.assertTrue(repr_str.startswith(start))
        self.assertTrue(repr_str.endswith(end))

        i = 0
        for key, value in eg_ac.items():
            i += 1
            findstr = "{}: {}".format(repr(key), repr(value))
            self.assertNotEqual(-1, repr_str.find(findstr))
            length += len(findstr) + 2

        self.assertEqual(i, 5)

        self.assertEqual(len(repr_str), length - 2)

    def test_copy (self):
        a = ArgumentCollector("a", "b", hi="hello", d="hey")
        a.update(1, 2, c=3, d=4)

        b = a.copy()
        self.assertEqual(a, b)
        self.assertEqual(len(a), len(b))

        for key in a:
            self.assertIn(key, b)
            self.assertEqual(a[key], b[key])

        for key in b:
            self.assertIn(key, a)
            self.assertEqual(a[key], b[key])

        b.update(3, 4)

        # a should be unchanged.
        self.assertEqual(a["a"], 1)
        self.assertEqual(a["b"], 2)
        self.assertEqual(a["c"], 3)
        self.assertEqual(a["d"], 4)
        self.assertEqual(a["hi"], "hello")

        # b should reflect the change (even with the default value for
        # "d").
        self.assertEqual(b["a"], 3)
        self.assertEqual(b["b"], 4)
        self.assertEqual(b["hi"], "hello")
        self.assertEqual(b["d"], "hey")

    def test_base (self):
        a = ArgumentCollector("a", z="zee")
        a.update(5)

        b = a.base("b")
        b.update(4)

        self.assertEqual(a, {
            "a":    5,
            "z":    "zee"})

        self.assertEqual(b, {
            "a":    5,
            "b":    4,
            "z":    "zee"})

        a.update(8)

        self.assertEqual(a["a"], 8)
        self.assertEqual(b["a"], 5)

        b.update(b=4, z="matt is cool")

        self.assertEqual(a["z"], "zee")
        self.assertEqual(b["z"], "matt is cool")

    def test_truthiness (self):
        a = ArgumentCollector("matt", matt="is cool")
        self.assertTrue(a)

        a = ArgumentCollector("hey", matt="is cool")
        self.assertFalse(a)

        a.update("holler")
        self.assertTrue(a)

        a = ArgumentCollector(matt="is still cool")
        self.assertTrue(a)

        a = ArgumentCollector()
        self.assertFalse(a)

        a.update(matt="just got cooler")
        self.assertTrue(a)

        a.update()
        self.assertFalse(a)

    def test_skip_iter (self):
        a = ArgumentCollector()
        a.skip_iter("hey", "matt")
        a.update(hey="hello", matt="is cool", ok="yes")

        self.assertEqual(len(a), 1)
        self.assertEqual(list(a), ["ok"])
        self.assertEqual(a["hey"], "hello")
        self.assertEqual(a["matt"], "is cool")
        self.assertEqual(a["ok"], "yes")

    def test_skip_iter_zero_length (self):
        a = ArgumentCollector()
        a.skip_iter("nothing")
        self.assertEqual(len(a), 0)
