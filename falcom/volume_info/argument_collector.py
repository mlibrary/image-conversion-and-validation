# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from collections.abc import Sequence, Mapping

from ..general.exceptions.type_errors import \
        MultipleValuesOneArgError, \
        MissingPositionalArgsError, \
        TooManyArgumentsError

class ArgumentCollector (Mapping):
    """Mapping that with unchanging default values that can only be
    modified with single `update` calls."""

    def __init__ (self, *args, **kwargs):
        """Initialize the argument collector with required and default
        values."""

        # The positional arguments are the names of the arguments our
        # update method will expect. The keyword arguments represent our
        # default values.
        self.__expected_args, self.__optional_args = \
                self.__get_args_and_kwargs(args, kwargs)

        # Otherwise, we start with no given arguments.
        self.__current_args = { }

        # We don't skip anything by default
        self.__skip = set()

    def update (self, *args, **kwargs):
        """Set a particular set of values.

        The expected positional arguments will match up with the
        positional arguments that you gave to init the object. Other
        than that, you can give whatever keyword arguments you want.

        Raises TypeError if you give weird arguments.
        """

        # First, make sure we can parse the new arguments without any
        # problems.
        mapping = self.__parse_new_args("update", args, kwargs)

        # We have a valid mapping, so we'll override whatever we used to
        # have.
        self.__current_args = mapping

    def copy (self):
        """Return a copy of this object.

        Altering the copy will not affect the original, and altering the
        original will not affect the copy. In other words, it's
        basically a deep copy, except much faster and without the memory
        cost.
        """

        # Create a new ArgumentCollector. Doesn't really matter how we
        # init it, since we're going to throw away its inards.
        result = ArgumentCollector()

        # Override its internals with our own. This is safe because
        # neither object has the ability to *modify* those internals;
        # updates merely replace them with new objects, which won't
        # affect other clones like these.
        result.__override_internals(self)

        return result

    def base (self, *args):
        """Return a new object defaulting to a copy of this one.

        It defaults to a copy so you won't have the ability to modify
        its default behavior by modifying the source object.
        """
        return ArgumentCollector(args, self.copy())

    def skip_iter (self, *args):
        """Set a list of keys to ignore on iteration and length
        checks."""
        self.__skip = set(args)

    def __getitem__ (self, key):
        """Return the value for the given key."""

        if key in self.__current_args:
            # Check the up-to-date given arguments first.
            return self.__current_args[key]

        else:
            # If it's not in there, try to use a default. If it's not in
            # there, we'll just pass along its KeyError.
            return self.__optional_args[key]

    def __iter__ (self):
        """Iterate through present keys."""

        # Skip any keys we don't want to iterate through.
        for key in self.__all_keys():
            if key not in self.__skip:
                yield key

    def __len__ (self):
        """Return the count of key-value pairs currently inside."""

        # Our length can start as the sum of our defaults and current
        # keypair lengths.
        result = len(self.__optional_args) + len(self.__current_args)

        for key in self.__current_args:
            if key in self.__optional_args:
                # If a key is in both, then we've counted it twice, so
                # we'll decrement our result to compensate.
                result -= 1

        for i in self.__skip:
            if i in self:
                result -= 1

        # We also want to subtract anything we're skipping.
        return result

    def __bool__ (self):
        """Return true if we contain values and if we contain all our
        required arguments."""

        if not self.__optional_args and not self.__current_args:
            # No need to waste time running len(self). We can just check
            # the two mappings directly. If they're both empty, then we
            # can return false, as expected.
            return False

        elif self.__current_args:
            # If we're here, it means we have some values. If there are
            # values in our current dict, we can assume they're valid
            # (and therefore account for all required arguments).
            return True

        else:
            # We have nonzero length, but we have no current dict, so I
            # don't know whether we're valid. I need to check for the
            # presence of each expected argument in order to be sure. If
            # they're all present, then we're valid.
            return all(arg in self for arg in self.__expected_args)

    def __repr__ (self):
        # I want to represent our mapping as a list of keypairs, so I
        # need a list.
        data = [ ]

        for key, value in self.items():
            # Add a string for each keypair, fully representing both the
            # key and the value, and making their relationship clear.
            data.append("{}: {}".format(repr(key), repr(value)))

        # Everything in that list should be comma-separated.
        return "<{} {{{}}}>".format(
                self.__class__.__name__, ", ".join(data))

    ################################################################
    ################ Private Properties and Methods ################
    ################################################################

    def __defaults_minus_current (self):
        # Loop through every key that isn't present in our current set
        # of values.
        for key in self.__optional_args:
            # Check every optional key.
            if key not in self.__current_args:
                # Only yield it if it hasn't been overridden by an
                # update().
                yield key

    def __get_args_and_kwargs (self, args, kwargs):
        # I want the user to have the ability to give args and kwargs as
        # premade arguments (rather than require variadic syntax).
        if len(args) == 2                           \
                and len(kwargs) == 0                \
                and isinstance(args[0], Sequence)   \
                and isinstance(args[1], Mapping):
            # If the user gave exactly two arguments, and those
            # arguments are a sequence and a mapping, then they must
            # have specified their args and kwargs.
            return args

        else:
            # Otherwise, assume they used the variadic syntax and return
            # these two as they are.
            return args, kwargs

    def __parse_new_args (self, function_name, args, kwargs):
        # We'll be returning a dict, and we start with a fresh one.
        mapping = { }

        # Be sure we're interpreting the arguments correctly and that
        # there aren't too many.
        args, kwargs = self.__validate_args_for_update(
                function_name, args, kwargs)

        self.__fill_in_all_args(function_name, args, kwargs, mapping)

        # Raise an exception if we're missing any required arguments.
        self.__raise_if_missing_args(function_name, mapping)

        return mapping

    def __validate_args_for_update (self, function_name, args, kwargs):
        # Be sure we have the genuine arguments.
        args, kwargs = self.__get_args_and_kwargs(args, kwargs)

        if len(args) > len(self.__expected_args):
            # If the positional argument list is longer than our list of
            # expected arguments, then we have too many arguments.
            raise TooManyArgumentsError(function_name, len(args))

        return args, kwargs

    def __fill_in_all_args (self, function_name, args, kwargs, mapping):
        # Pull out any positional arguments.
        self.__fill_in_positional_args(
                function_name, args, kwargs, mapping)

        # Fill in the remaining (keyword) arguments.
        mapping.update(kwargs)

    def __fill_in_positional_args (self,
            function_name, args, kwargs, mapping):
        # We'll loop through the expected argument keys in step with our
        # positional arguments to get key-value pairs.
        for key, value in zip(self.__expected_args, args):
            # Raise an error if this key is used positionally *and* as
            # an explicit keyword.
            self.__raise_if_duplicate_key(function_name, key, kwargs)

            # If we're ok, add the keypair.
            mapping[key] = value

    def __raise_if_duplicate_key (self, function_name, key, kwargs):
        if key in kwargs:
            # We received this key as a positional argument, and now a
            # second time as a keyword argument. That means we've
            # received multiple values with one key.
            raise MultipleValuesOneArgError(function_name, key)

    def __raise_if_missing_args (self, function_name, mapping):
        # Get a list of all missing keys.
        missing = self.__find_any_missing_args(mapping)

        if missing:
            # If we found any, raise an error.
            raise MissingPositionalArgsError(function_name, *missing)

    def __find_any_missing_args (self, mapping):
        missing = [ ]

        for key in self.__expected_args:
            # Look at each key we expect to see.
            self.__add_key_if_missing(key, mapping, missing)

        return missing

    def __add_key_if_missing (self, key, mapping, missing):
        if key not in mapping:
            # If this key isn't in our mapping, it's missing.
            missing.append(key)

    def __override_internals (self, source):
        assert isinstance(source, ArgumentCollector)

        # Change every aspect of our own identity to match that of this
        # new source.
        self.__expected_args = source.__expected_args
        self.__optional_args = source.__optional_args
        self.__current_args = source.__current_args

    def __all_keys (self):
        # First, iterate through any defaults that aren't overridden.
        # Second, iterate through the current specified set.
        yield from self.__defaults_minus_current()
        yield from self.__current_args
