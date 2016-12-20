# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from collections.abc import Sequence, Mapping
from re import compile as re_compile
from urllib.parse import urlencode
from urllib.request import urlopen

########################################################################
############################## Exceptions ##############################
########################################################################

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

        return TypeError("hello() missing {}: {}".format(
                missing(len(args)), " and ".join(map(repr, args))))

########################################################################
############################### Classes ################################
########################################################################

class TabularData (Sequence):
    """A class to parse input files and hold their data meaningfully.

    You give it the path to an input file, and it opens, reads, parses,
    and closes that file. For the most part, it acts like a read-only
    list of tuples.

    Each row (i.e. each tuple in the list) will have the same length,
    and that length will equal `self.cols`.

    Since I already have `self.cols`, you can also access `self.rows`,
    which in turn simply calls `len(self)`. Its purpose is purely
    semantic.

    Lastly, you can set the `self.header` flag (which is `False` by
    default), and the first row will be deleted for all intents and
    purposes. You can undo this deletion by setting it back to `False`.

    For example, let's say we have this tab-delimited file with three
    columns:

        barcode         nickname    status
        39015000000011  hello       DC
        39015000000029  holler      DC
        39015000000037  sup, hi     DC
        39015000000045  WHAT NEWS   DC

    Here are some example manipulations (with minor whitespace
    alterations for the sake of readability):

        >>> data = TabularData("path_to_above_file.txt")
        >>> # You can view a repr that shows everything inside.
        ... data
        <TabularData header=False ('barcode', 'nickname', 'status'),
                                  ('39015000000011', 'hello', 'DC'),
                                  ('39015000000029', 'holler', 'DC'),
                                  ('39015000000037', 'sup, hi', 'DC'),
                                  ('39015000000045', 'WHAT NEWS', 'DC')>
        >>> # You can access each row as if this were a list.
        ... data[0]
        ('barcode', 'nickname', 'status')
        >>> data[1]
        ('39015000000011', 'hello', 'DC')
        >>> data[2]
        ('39015000000029', 'holler', 'DC')
        >>> data[3]
        ('39015000000037', 'sup, hi', 'DC')
        >>> data[4]
        ('39015000000045', 'WHAT NEWS', 'DC')
        >>> # You can also access from the end using negative numbers,
        ... # same as any.
        ... data[-1]
        ('39015000000045', 'WHAT NEWS', 'DC')
        >>> data[-5]
        ('barcode', 'nickname', 'status')
        >>> # Slice notation will work as expected, returning a list.
        ... data[:]
        [('barcode', 'nickname', 'status'),
         ('39015000000011', 'hello', 'DC'),
         ('39015000000029', 'holler', 'DC'),
         ('39015000000037', 'sup, hi', 'DC'),
         ('39015000000045', 'WHAT NEWS', 'DC')]
        >>> # You can get the length, same as any, but you can also
        ... # specifically get the count of rows and/or columns. The
        ... # length matches the row count.
        ... len(data)
        5
        >>> data.rows
        5
        >>> data.cols
        3
        >>> # By default, we assume that the data has no header row.
        ... data.header
        False
        >>> # However, you can set it to True, and the dataset will
        ... # behave very differently.
        ... data.header = True
        >>> # That said, the repr doesn't look too different.
        ... data
        <TabularData header=True ('barcode', 'nickname', 'status'),
                                 ('39015000000011', 'hello', 'DC'),
                                 ('39015000000029', 'holler', 'DC'),
                                 ('39015000000037', 'sup, hi', 'DC'),
                                 ('39015000000045', 'WHAT NEWS', 'DC')>
        >>> # We now have four rows instead of five.
        ... len(data)
        4
        >>> data.rows
        4
        >>> data.cols
        3
        >>> # If you look at the first row now, you'll see that we're
        ... # skipping the header row, diving right into the data.
        ... data[0]
        ('39015000000011', 'hello', 'DC')
        >>> # Even if we get a slice of everything, the header row is
        ... # gone.
        ... data[:]
        [('39015000000011', 'hello', 'DC'),
         ('39015000000029', 'holler', 'DC'),
         ('39015000000037', 'sup, hi', 'DC'),
         ('39015000000045', 'WHAT NEWS', 'DC')]
        >>> # There is really no way to access that header row if the
        ... # header flag is set.
        ... data[4]
        Traceback (most recent call last):
          [...]
        IndexError: list index out of range
        >>> data[-5]
        Traceback (most recent call last):
          [...]
        IndexError: list index out of range
        >>> # But the header row hasn't actually been deleted: you can
        ... # bring it back any time by unsetting the header flag.
        ... data.header = False
        >>> data[0]
        ('barcode', 'nickname', 'status')
    """

    @property
    def rows (self):
        """Return the number of rows."""

        # The rowcount matches the length.
        return len(self)

    @property
    def cols (self):
        """Return the number of columns."""

        if len(self) == 0:
            # We have no columns if we have no rows.
            return 0

        else:
            # The colcount matches the length of the first row.
            return len(self[0])

    def __init__ (self, path_to_file):
        """Initialize input data based on path to file.

        Raises InputFileError or OSError.
        """

        # I want to store the path to the file.
        self.path = path_to_file

        # By default, we do not have a header row.
        self.header = False

        # Open the file.
        self.__open_file()

    def __getitem__ (self, key):
        """Return the row at the given index."""

        if self.header:
            # We need to do some special handwaving if we have a header
            # row.
            return self.__getitem_but_skip_header(key)

        else:
            # If we don't have a header row, then the first row comes
            # first like normal.
            return self.__rows[key]

    def __len__ (self):
        """Return the number of rows."""

        if self.header:
            # If we have a header row, then we don't count it in our
            # length.
            return max(0, len(self.__rows) - 1)

        else:
            # If there's no header row, then we pass on the length
            # as-is.
            return len(self.__rows)

    def __repr__ (self):
        # Whether there's a header is part of our deal here.
        result = "<{} header={}".format(self.__class__.__name__,
                                        repr(self.header))

        if len(self.__rows) > 0:
            # Each row should be separated by a comma-space.
            result += " " + ", ".join(map(repr, iter(self.__rows)))

        # Whether or not we added rows, we close the repr string with a
        # closing angle bracket.
        return result + ">"

    def __iter__ (self):
        """Iterate through rows.

        This overrides the default __iter__ method. By default, it'd run
        self.__getitem__(), and it'd run it self.__len__() times. Both
        methods check self.header, which won't (or at least shouldn't)
        change during an iteration.

        So I figure it's fastest to only check once and iterate through
        the internal list accordingly.
        """

        if self.header:
            # If there's a header row, then we'll skip the first row.
            return iter(self.__rows[1:])

        else:
            # If not, we loop over the entire thing.
            return iter(self.__rows)

    ################################################################
    ################ Private Properties and Methods ################
    ################################################################

    __encodings = (
        # I generally hope for UTF-8. Everything *should* be UTF-8.
        "utf-8",

        # If not UTF-8, Codepage 1252 is always a possibility.
        "cp1252",

        # I could go for latin1 (iso 8859-1), but that will accept
        # literally any bytestring, and I think it's important that this
        # have the ability to fail.
    )

    # If I'm expecting CRLF newlines, then (a) all CRs must be followed
    # by LFs and (b) all LFs must be preceded by CRs.
    __re_not_crlf = re_compile(r"\r[^\n]|[^\r]\n")

    # I'm considering all control characters (except HT and LF, that is,
    # 0x09 and 0x0a) to be invalid.
    __re_bad_controls = re_compile(r"[\0-\x08\x0b-\x1f\x7f-\x9f]")

    def __open_file (self):
        with open(self.path, "rb") as input_file:
            # Read the entire contents of the file into memory.
            bytes_obj = input_file.read()

        # Convert the bytes object to str.
        text = self.__bytes_to_str(bytes_obj)

        # We have a valid unicode str. All that's left is to parse it
        # into rows of columns.
        self.__parse_text(text)

    def __bytes_to_str (self, bytes_obj):
        # Figure out the bytestring's encoding, and use that to convert
        # to unicode.
        result = self.__find_unicode(bytes_obj)

        # Clean up weird newlines.
        result = self.__clean_newlines(result)

        # Control characters (other than HT and LF) are signs of weird
        # encoding issues that may not have been caught by using the
        # 1252 codepage.
        self.__error_on_control_characters(result)

        return result

    def __find_unicode (self, bytes_obj):
        for encoding in self.__encodings:
            # Check each expected encoding.
            result = self.__attempt_decode(bytes_obj, encoding)

            if result is not None:
                # If we got a non-None result, then we succeeded!
                return result

        # If we never got a unicode str object, then we should raise
        # a unicode error.
        raise CantDecodeEncoding(self.path)

    def __attempt_decode (self, bytes_obj, encoding):
        # Set our encoding.
        self.encoding = encoding

        try:
            # Try to decode the bytestring assuming that encoding.
            return bytes_obj.decode(encoding)

        except UnicodeDecodeError:
            # If we can't, then we don't return anything after all.
            return None

    def __clean_newlines (self, result):
        if "\r" in result:
            # If there are carriage returns, then we need to deal with
            # them.
            return self.__deal_with_CR(result)

        else:
            # If not, then awesome! Looks like we already only have
            # linefeeds.
            return result

    def __deal_with_CR (self, result):
        if "\n" in result:
            # We have carriage returns. If we also have linefeeds, then
            # we *should* be dealing with CRLF newlines. That said,
            # we'll want to check.
            return self.__deal_with_CRLF(result)

        else:
            # If we have carriage returns without linefeeds, then all we
            # need to do is replace them. There's no confusion.
            return result.replace("\r", "\n")

    def __deal_with_CRLF (self, result):
        # See if we can find a lone CR or LF in here.
        match = self.__re_not_crlf.search(result)

        if match is not None:
            # We have text containing at least one CR and at least one
            # LF, and at least one of those is on its own (i.e. not part
            # of a CRLF).
            #
            # It's not hopeless, but whatever's going on likely
            # necessitates further investigation by hand to fix the
            # problem.
            raise InconsistentNewlines(self.path)

        else:
            # All newlines are CRLFs, so it's time to replace each with
            # an LF.
            return result.replace("\r\n", "\n")

    def __error_on_control_characters (self, result):
        # Try and find any control character.
        match = self.__re_bad_controls.search(result)

        if match is not None:
            # We found one! That's tooooo bad.
            raise InvalidControls(ord(match.group(0)), self.path)

    def __parse_text (self, text):
        # Our internal row storage starts with no data.
        self.__rows = [ ]

        # Split the full text into a list of lines.
        str_rows = text.strip("\n").split("\n")

        # str.split() always returns a list of at least one item, so I'm
        # guaranteed to have a row at index 0. However, given that I
        # stripped newlines before splitting, the first line will only
        # be blank if I have no data at all. So I only move forward if
        # the first line has data.
        if len(str_rows[0]) > 0:
            # If we have rows to append, append them.
            self.__append_rows(str_rows)

    def __append_rows (self, str_rows):
        # The column-count of the first row sets the tone for subsequent
        # rows.
        num_cols = len(str_rows[0].split("\t"))

        for str_row in str_rows:
            # We'll look at each row alongside our expected length.
            self.__append_row_if_valid(str_row, num_cols)

    def __append_row_if_valid (self, str_row, num_cols):
        # Rather than a *list* of columns, I'll split the row into a
        # *tuple* of columns. They're presently split by HTs.
        row = tuple(str_row.split("\t"))

        if len(row) == num_cols:
            # This row is an expected length, so all that's left is to
            # append it to our internal list of rows.
            self.__rows.append(row)

        else:
            # This row isn't the same length as the first row. That
            # means we have inconsistent column counts in this file, and
            # we can't use it.
            raise InconsistentColumnCounts(self.path)

    def __getitem_but_skip_header (self, key):
        if isinstance(key, slice):
            # If we've been given a slice, the easiest thing to do is
            # take two slices -- the first one will slice out the header
            # row, and then the second can act as it will.
            return self.__rows[1:][key]

        else:
            # Otherwise, we've probably been given an integer. Taking a
            # slice would be overkill in this case, so we do our own
            # thing.
            return self.__getitem_with_int_key(key)

    def __getitem_with_int_key (self, key):
        if key >= 0:
            # Given a normal, nonnegative index, we simply increment it
            # to ensure that we skip the first row.
            return self.__rows[key + 1]

        elif key + len(self.__rows) == 0:
            # If we have a negative index, then we want to check to see
            # if it would normally point at the header row. If it would,
            # we'll decrement it to force it to be out of range.
            return self.__rows[key - 1]

        else:
            # Otherwise, we have a negative index that won't point at
            # the header row. Therefore, we can just pass it along. The
            # last row is still the last row.
            return self.__rows[key]

class ArgumentCollector (Mapping):
    """Mapping that with unchanging default values that can only be
    modified with single `update` calls."""

    def __init__ (self, *args, **kwargs):
        """Initialize the argument collector with required and default
        values."""

        # Be sure we have the genuine arguments.
        args, kwargs = self.__get_args_and_kwargs(args, kwargs)

        # The positional arguments are the names of the arguments our
        # update method will expect.
        self.__expected_args = args

        # The keyword arguments represent our default values.
        self.__optional_args = kwargs

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
            self.__raise_too_many_arguments(function_name, len(args))

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
            self.__raise_multiple_values_one_key(function_name, key)

    def __raise_if_missing_args (self, function_name, mapping):
        # Get a list of all missing keys.
        missing = self.__find_any_missing_args(mapping)

        if missing:
            # If we found any, raise an error.
            self.__raise_missing_args(function_name, missing)

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

    def __raise_missing_args (self, function_name, missing):
        # Raise the error message using an english list of reprs of the
        # missing keys.
        self.__raise_missing_positional_args(
                function_name,
                len(missing),
                self.__english_repr_list(missing))

    def __english_repr_list (self, elts):
        if len(elts) > 2:
            # If we have more than two items, then we want everything
            # separated by commas with a trailing "and" before the last
            # item.
            return "{}, and {}".format(
                    ", ".join(map(repr, elts[:-1])),
                    repr(elts[-1]))

        else:
            # If we have two items or fewer, we don't need commas. Since
            # there are only three possible cases, I'll just list them:
            #
            #     []        => ""
            #     [a]       => "repr(a)"
            #     [a, b]    => "repr(a) and repr(b)"
            return " and ".join(map(repr, elts))

    def __maybe_plural (self, n, word, plural = None):
        if n == 1:
            # If there's just 1, then we don't need to care about the
            # plural at all.
            return "1 " + word

        else:
            # Otherwise, we may need to add an s to the word, depending
            # on whether we were actually given a plural alternative.
            return "{:d} {}".format(n, self.__add_s(word, plural))

    def __add_s (self, word, plural):
        if plural is None:
            # By default, the plural just adds an s.
            return word + "s"

        else:
            # Otherwise, we default to whatever the user says.
            return plural

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

    def __raise_too_many_arguments (self, function_name, args_length):
        raise TypeError("{}() takes {} but {} given".format(
                function_name,
                self.__maybe_plural(
                        len(self.__expected_args),
                        "positional argument"),
                self.__maybe_plural(args_length, "was", "were")))

    def __raise_multiple_values_one_key (self, function_name, key):
        raise TypeError(
                "{}() got multiple values for argument {}".format(
                        function_name,
                        repr(key)))

    def __raise_missing_positional_args (self,
            function_name, count, arg_str):
        raise TypeError("{}() missing {}: {}".format(
                function_name,
                self.__maybe_plural(count,
                        "required positional argument"),
                arg_str))

class DecoyMapping (Mapping):
    """Pretends to be a mapping but tracks queries and returns 0.

    This is nice if you need to know exactly which keys are queried.
    """

    def __init__ (self, value = 0):
        """Init an empty decoy mapping."""

        # Start with an empty set.
        self.__keys = set()
        self.__value = value

    def get_keys (self):
        """Return the set of keys."""
        return self.__keys

    def __getitem__ (self, key):
        """Add key and return 0."""

        # A query! Add this to our set.
        self.__keys.add(key)

        # Return 0. Probably safe.
        return self.__value

    def __len__ (self):
        """Return 0."""
        return 0

    def __iter__ (self):
        """Return an empty iterator."""
        return iter(())

def extract_format_keys (s):
    """Return the set of named keywords in the format string."""

    # Use a decoy mapping to track whatever we're asking for.
    mapping = DecoyMapping()

    # We use format map to stop the thing from trying to convert to a
    # dict or anything weird.
    junk = s.format_map(mapping)

    # Return the resulting set of keys.
    return mapping.get_keys()

class URI:
    """URI object that handles GET and/or POST data."""

    def __init__ (self, *args, **kwargs):
        """Init URI with base, expected args, and default data."""

        # The base URI should be the first positional argument.
        self.__uri = self.__extract_uri(args)

        # For everything else, we use an ArgumentCollector.
        self.__args = ArgumentCollector(args[1:], kwargs)

        # I don't want the arguments to iterate through any format names
        # that happen to be in the URI.
        self.__args.skip_iter(*tuple(
                extract_format_keys(self.__uri.decode("ascii"))))

    def get (self, *args, **kwargs):
        """Return an HTTPResponse for the given GET request."""

        # We store URIs as bytes objects, so we need to decode it to an
        # ASCII str.
        return urlopen(self.get_uri(*args, **kwargs).decode("ascii"))

    def post (self, *args, **kwargs):
        """Return an HTTPResponse for the given POST request."""

        uri, data = self.post_uri(*args, **kwargs)

        # We store URIs as bytes objects, so we need to decode it to an
        # ASCII str.
        return urlopen(uri.decode("ascii"), data)

    def get_uri (self, *args, **kwargs):
        """Return a URI bytes object with appropriate GET data."""

        # Get the data.
        uri, data = self.post_uri(*args, **kwargs)

        if data:
            # If we have any data, it's appended to the URI with a
            # question mark.
            return uri + b"?" + data

        else:
            # If we have no data, we can just use the URI as-is.
            return uri

    def post_uri (self, *args, **kwargs):
        """Return a duple of bytes objects: base URI and POST data."""
        # Get the data.
        data = self.__get_encoded_data(args, kwargs)

        # Get the specific URI.
        uri = self.__uri.decode("ascii").format_map(
                self.__args).encode("ascii")

        return uri, data

    ################################################################
    ################ Private Properties and Methods ################
    ################################################################

    def __extract_uri (self, positional_args):
        if positional_args:
            # If we have any arguments, then we're looking at the first
            # one. It needs to be ASCII bytes.
            return self.__assert_bytes(positional_args[0])

        else:
            # If we don't have any positional arguments, it's time to
            # raise a TypeError telling the user about it.
            #
            # Normally, it'd be better to explicitly include a named
            # argument "uri_base" in the function, but I don't want to
            # limit the names of keyword arguments. If I put that there,
            # and one of the keyword arguments was keyed on uri_base,
            # then it'd override that instead of being passed on to the
            # argument collector.
            raise TypeError("__init__() missing 1 required " \
                    "positional argument: 'uri_base'")

    def __get_encoded_data (self, args, kwargs):
        # Update our internal argument collector.
        self.__args.update(args, kwargs)

        # Run urllib.parse.urlencode on the mapping.
        encoded = urlencode(self.__args)

        # We might get a str, and we want bytes.
        return self.__assert_bytes(encoded)

    def __assert_bytes (self, ascii_str):
        if isinstance(ascii_str, bytes):
            # If it's already bytes, we'll just assume it's all ASCII.
            return ascii_str

        else:
            # If it's a str, we'll need to encode it into bytes.
            return ascii_str.encode("ascii")
