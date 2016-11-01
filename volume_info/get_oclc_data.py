# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from collections.abc import Sequence
from re import compile as re_compile

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

########################################################################
############################### Classes ################################
########################################################################

class InputData (Sequence):
    """A class to parse input files and hold their data meaningfully."""

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

    def __init__ (self, path_to_file):
        """Initialize input data based on path to file.

        Raises InputFileError or OSError.
        """

        # I want to store the path to the file.
        self.path = path_to_file

        # Open the file.
        self.__open_file()

    def __getitem__ (self, key):
        return self.__rows[key]
    def __len__ (self):
        return len(self.__rows)

    @property
    def rows (self):
        # The rowcount matches the length.
        return len(self)

    @property
    def cols (self):
        if len(self) == 0:
            # We have no columns if we have no rows.
            return 0

        else:
            # The colcount matches the length of the first row.
            return len(self[0])

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
