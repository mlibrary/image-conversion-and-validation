# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from collections.abc import Sequence
from re import compile as re_compile

from ..exceptions import BaseError

class TabularData (Sequence):
    """Parse tabular input files and hold their data."""

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
        raise self.CantDecodeEncoding(self.path)

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
            raise self.InconsistentNewlines(self.path)

        else:
            # All newlines are CRLFs, so it's time to replace each with
            # an LF.
            return result.replace("\r\n", "\n")

    def __error_on_control_characters (self, result):
        # Try and find any control character.
        match = self.__re_bad_controls.search(result)

        if match is not None:
            # We found one! That's tooooo bad.
            raise self.InvalidControls(ord(match.group(0)), self.path)

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
            raise self.InconsistentColumnCounts(self.path)

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
