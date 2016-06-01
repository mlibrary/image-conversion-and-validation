#!/usr/bin/env python3
from collections        import  namedtuple
from itertools          import  count
from os.path            import  isdir, isfile, join as os_path_join,   \
                                split as os_path_split
from re                 import  compile as re_compile, MULTILINE
from subprocess         import  Popen, PIPE
import xml.etree.ElementTree as ET

# This appears on the help print screen.
DETAILED_DESCRIPTION    = """\
Convert pageview.dat files to meta.yml files."""

# These are the files we'll mainly be dealing with.
PAGEVIEW_DAT_FILENAME   = "pageview.dat"
META_YML_FILENAME       = "meta.yml"

# Page image filenames look like eight-digit numbers, but technically,
# the first zero is a prefix (which could be such as a `p` or who knows
# what else under some circumstances).
PAGE_IMAGE_FORMAT       = "0{num:07d}.{ext}".format

# We'll use YYYY-mm-ddTHH:MM:SS-05:00. I could probably do better, all
# looking at timezones and etc, but not now.
SCAN_DATE_FORMAT        = "{}-{}-{}T{}:{}:{}-05:00".format

DEFAULT_CAPTURE_AGENT   = "MiU"
DEFAULT_READING_ORDER   = "left-to-right"

# Colorful output.
def echogood (message):
    print("\x1b[1;32m *\x1b[0m " + message)
def echowarn (message):
    print("\x1b[1;33m *\x1b[0m " + message)
def echobad (message):
    print("\x1b[1;31m *\x1b[0m " + message)

########################################################################
############################## Exceptions ##############################
########################################################################

class PageviewToMetaError (RuntimeError):
    pass

class NoDirectoryError (PageviewToMetaError):
    def __init__ (self, path):
        self.path   = path
    def __str__ (self):
        return "not a directory: {}".format(self.path)

class NoFileError (PageviewToMetaError):
    def __init__ (self, path):
        self.path   = path
    def __str__ (self):
        return "not a file: {}".format(self.path)

class NoneAreFiles (PageviewToMetaError):
    def __init__ (self, list_of_paths):
        self.paths  = list_of_paths
    def __str__ (self):
        return "none are files: {}".format(", ".join(self.paths))

class ExpectedFiveColumns (PageviewToMetaError):
    def __init__ (self, path, line_number):
        self.path           = path
        self.line_number    = line_number
    def __str__ (self):
        return "expected five columns on line {:d}: {}".format(
                path, line_number)

class CouldntParseLine (PageviewToMetaError):
    def __init__ (self, path, line_number):
        self.path           = path
        self.line_number    = line_number
    def __str__ (self):
        return "unable to parse line {:d}: {}".format(path,
                                                      line_number)

class UnexpectedPageSequence (PageviewToMetaError):
    def __init__ (self, sequence):
        self.sequence   = sequence
    def __str__ (self):
        return "unexpected page sequence number: {:08d}".format(
                                                    self.sequence)

class FoundSequenceSkip (PageviewToMetaError):
    def __init__ (self, sequence):
        self.sequence   = sequence
    def __str__ (self):
        return "sequence skip: {:08d}".format(self.sequence)

class ExifToolFailed (PageviewToMetaError):
    errorstring = "exiftool failed to read {}"

    def __init__ (self, path_to_image, stderr = ""):
        self.path_to_image  = path_to_image
        self.stderr         = stderr
    def __str__ (self):
        print(self.stderr)
        return self.errorstring.format(self.path_to_image)

class ExifToolReturnedBadXML (ExifToolFailed):
    errorstring = "exiftool returned invalid XML for {}"

class InvalidDate (PageviewToMetaError):
    def __init__ (self, date):
        self.date   = date
    def __str__ (self):
        return "unrecognized date format: {}".format(repr(self.date))

class InvalidFilename (PageviewToMetaError):
    def __init__ (self, path_to_volume, filename):
        self.path_to_volume = path_to_volume
        self.filename       = filename
    def __str__ (self):
        return "In {} pageview, invalid page filename: {}".format(
                self.path_to_volume, self.filename)

class MismatchedFilenameAndSequence (PageviewToMetaError):
    def __init__ (self, path_to_volume, filename, sequence):
        self.path_to_volume = path_to_volume
        self.filename       = filename
        self.sequence       = sequence
    def __str__ (self):
        return "In {} pageview, mismatched {} and {}".format(
                self.path_to_volume,
                self.filename,
                self.sequence)

########################################################################
############################### Functors ###############################
########################################################################

class ArgumentParserBuilder:
    # These are the reading order strings in full.
    left_to_right   = "left-to-right"
    right_to_left   = "right-to-left"

    def __call__ (self, parser):
        # Grab the argument parser.
        self.parser = parser

        # Add positional arguments then optional ones.
        self.add_positional_arguments()
        self.add_optional_arguments()

        # Return the updated parser.
        return self.parser

    def add_positional_arguments (self):
        # The only positional arguments are the list of volume
        # directories (which must have a length of at least one).
        self.parser.add_argument("volumes",
                                 nargs      = "+",
                                 help       = "paths to volume dirs")

    def add_optional_arguments (self):
        # The optional arguments are the capture agent and the reading
        # order.
        self.add_agent()
        self.add_all_reading_orders()

    def add_agent (self):
        # Let's tell the user our default capture agent.
        help_text   = "capture agent (default: {})".format(
                                            DEFAULT_CAPTURE_AGENT)

        self.parser.add_argument("-a", "--agent",
                                 default    = DEFAULT_CAPTURE_AGENT,
                                 help       = help_text)

    def add_all_reading_orders (self):
        # There are two reading orders. At the moment, I do nothing to
        # distinguish between reading and scanning order because
        # everything we do has matching scanning and reading orders.
        self.add_reading_order(self.right_to_left,
                               "set right-to-left reading order")
        self.add_reading_order(self.left_to_right,
                               "set left-to-right reading order")

    def add_reading_order (self, value, help_text):
        if value == DEFAULT_READING_ORDER:
            # If this one is the default value, append it to the help
            # text.
            help_text += " (default)"

        self.parser.add_argument("--" + value,
                                 dest       = "reading_order",
                                 action     = "store_const",
                                 const      = value,
                                 default    = DEFAULT_READING_ORDER,
                                 help       = help_text)

class PageviewDatParser:
    # Each line in a pageview.dat file has five values in this order.
    PageviewTuple       = namedtuple("PageviewTuple", ("filename",
                                                       "sequence",
                                                       "page_number",
                                                       "confidence",
                                                       "page_feature"))

    # A line consisting of only whitespace (and possibly a comment)
    # counts as a comment line.
    re_comment_line     = re_compile(r"^\s*(#.*)?$")

    def __call__ (self, path_to_pageview):
        # I'll want the path to the pageview.
        self.path_to_pageview   = path_to_pageview

        # Internal parameters set, we parse the pageview.dat file.
        self.parse_pageview_file()

        # We'll be returning the list of sorted data.
        return self.sorted_data

    def parse_pageview_file (self):
        # Initialize a new dict.
        self.pageview_data          = { }

        for line, line_number in zip(self.get_list_of_lines(),
                                     count(1)):
            # Add each line to the internal dict, one at a time.
            self.add_line_to_dict(line, line_number)

        # Now that we're done, be sure no pages got skipped. This will
        # sort the data as well, since we need it to be in order to
        # detect page skips.
        self.assert_no_page_skips()

    def assert_no_page_skips (self):
        # I'll need a sorted list of sequences.
        self.sort_the_data()

        for sequence, expected in zip(self.sorted_sequences,
                                      count(1)):
            # We have a sequence number and an expected sequence number.
            # They should always match.
            if sequence != expected:
                # If they don't match, we raise an error.
                self.raise_sequence_skip(sequence, expected)

    def raise_sequence_skip (self, sequence, expected):
        if sequence < expected:
            # I've already checked to be sure there are no duplicates,
            # so the only way I can think of this happening would be
            # negative numbers or zero. Whatever it is though, it's not
            # a page sequence I expected to see.
            raise UnexpectedPageSequence(sequence)

        else:
            # Otherwise, the actual sequence number is bigger than
            # expected, which means it must have skipped a page. We'll
            # raise the exception with the expected value, since it's
            # the one that must be missing.
            raise FoundSequenceSkip(expected)

    def sort_the_data (self):
        # I need to be sure the sequence numbers have been sorted. This
        # also resets the sorted data list.
        self.sort_the_sequence_numbers()

        for sequence in self.sorted_sequences:
            # Now that I have a sequence, I also want the four values
            # that go with it.
            filename, page_number, confidence, page_feature \
                    = self.pageview_data[sequence]

            # Finally, I can make the named tuple that gotham needs. It
            # gets appended to our sorted data list.
            self.sorted_data.append(self.PageviewTuple(filename,
                                                       sequence,
                                                       page_number,
                                                       confidence,
                                                       page_feature))

    def sort_the_sequence_numbers (self):
        # Get the sequence numbers. Sort that list.
        self.sorted_sequences       = list(self.pageview_data)
        self.sorted_sequences.sort()

        # I'll want to set the sorted data to an empty list.
        self.sorted_data            = [ ]

    def line_is_not_a_comment (self, line):
        # If it matches, it's a comment. If it returns None, it's not.
        return self.re_comment_line.match(line) is None

    def add_line_to_dict (self, line, line_number):
        # We'll only do anything if this line isn't a comment.
        if self.line_is_not_a_comment(line):
            # Get the key (the sequence) and the other values.
            sequence, value_tuple   = self.parse_line(line, line_number)

            # Assert that we don't have a duplicate sequence number.
            self.assert_sequence_not_in_pageview_data(sequence)

            # Cool! Go on and insert the value tuple.
            self.pageview_data[sequence] = value_tuple

        # I don't need an "else" clause because I can just ignore
        # comments.

    def assert_sequence_not_in_pageview_data (self, sequence):
        if sequence in self.pageview_data:
            # Found a duplicate.
            raise FoundSameSequenceTwice(self.path_to_pageview,
                                         sequence)

    def parse_line (self, line, line_number):
        # Cells are separated by horizontal tabs.
        cells                   = line.split("\t")

        if len(cells) != 5:
            # There should be five columns. I could allow four and
            # assume a blank feature, but nah. Let's be strict.
            raise ExpectedFiveColumns(self.path_to_pageview,
                                      line_number)

        # Now that I have a list of cells, I need to turn them into
        # values.
        return self.parse_five_cells(cells, line_number)

    def parse_five_cells (self, cells, line_number):
        try:
            # I'm in a `try` block, so it's safe to get the tuple
            # without any error-checking.
            return self.get_key_value_tuple(cells)

        except:
            # If it didn't work, I'll let the user figure out exactly
            # why it didn't work by giving them the file and the line
            # number.
            raise CouldntParseLine(self.path_to_pageview, line_number)

    def get_key_value_tuple (self, cells):
        # We return the key and a value quadruple. Note that this isn't
        # quite in the pageview.dat order: our key (the page sequence)
        # is the second value in the list of cells. We'll move it back
        # once I've asserted an order.
        return (int(cells[1].lstrip("0")),      # Page sequence (int)
                (cells[0],                      # Filename      (str)
                 cells[2].lstrip("0"),          # Page number   (str)
                 self.get_confidence(cells[3]), # Confidence    (int)
                 cells[4]))                     # Page feature  (str)

    def get_confidence (self, confidence_str):
        if confidence_str == "":
            # If there's no confidence value, we'll just call it 100.
            return 100

        else:
            # Otherwise, it should be an integer.
            return int(confidence_str)

    def get_list_of_lines (self):
        # Open and read the file, and then close it.
        file_object             = open(self.path_to_pageview, "r")
        file_content            = file_object.read()
        file_object.close()

        # Split the file content into lines.
        return self.split_into_lines(file_content)

    def split_into_lines (self, text):
        # Replace CRLFs with LFs, then replace CRs with LFs. That way
        # each line is separated by linefeeds only. Then we just split
        # into a list, separated by linefeeds. I won't strip out
        # trailing newlines or anything because blank lines are totally
        # something I can handle.
        return text.replace("\r\n", "\n")   \
                   .replace("\r",   "\n")   \
                   .split("\n")

class PageviewFilenameValidator:
    re_filename = re_compile(r"^0([0-9]{7})\.(tif|jp2)$")
    seq_to_str  = "{:07d}".format

    def __call__ (self, path_to_volume, pageview_data):
        # We'll keep the path to the volume internally.
        self.path_to_volume = path_to_volume

        for filename, sequence, page_number, confidence, page_feature \
                in pageview_data:
            # Validate each row. The page number, confidence, and page
            # feature should all be valid already, so the only fields
            # we're really interested in are the filename and sequence.
            self.validate_row(filename, sequence)

    def validate_row (self, filename, sequence):
        # The sequence numbers are already guaranteed to be in order,
        # without duplicates or skips, and one-indexed. All that's left
        # is to make sure they match the filename.
        self.assert_matching_numbers(filename, sequence)

        # We should also be sure the file exists.
        self.assert_file_exists(filename)

    def assert_matching_numbers (self, filename, sequence):
        match   = self.re_filename.match(filename)

        if match is None:
            raise InvalidFilename(self.path_to_volume, filename)

        if match.group(1) != self.seq_to_str(sequence):
            raise MismatchedFilenameAndSequence(
                    self.path_to_volume, filename, sequence)

    def assert_file_exists (self, filename):
        full_path   = os_path_join(self.path_to_volume, filename)

        if not isfile(full_path):
            raise NoFileError(full_path)

class ExifDateGetter:
    date_xpaths = (
        ".//{http://ns.exiftool.ca/XMP/XMP-tiff/1.0/}DateTime",
        ".//{http://ns.exiftool.ca/EXIF/IFD0/1.0/}ModifyDate",
    )

    re_date     = re_compile(r"(?P<year>\d{4})[-:/]"
                             r"(?P<month>\d{2})[-:/]"
                             r"(?P<day>\d{2})[ T]"
                             r"(?P<hour>\d{2}):"
                             r"(?P<minute>\d{2})"
                             r"(?::(?P<second>\d{2}))?")

    def __init__ (self, scan_date_format = SCAN_DATE_FORMAT):
        # We'll let the user mess with this format if they need to for
        # some reason.
        self.scan_date_format   = scan_date_format

    def __call__ (self, path_to_image):
        # We'll want to store the path to the image.
        self.path_to_image  = path_to_image

        # Then all we have to do is run exiftool.
        return self.get_date()

    def get_date (self):
        # Get the Popen object for the exiftool process.
        popen_object    = self.init_popen_object()

        # Grab the standard output and standard error.
        stdout, stderr  = popen_object.communicate()

        # Assert that exiftool thinks it did a good job. In case it
        # didn't, we'll also pass the standard error string in hopes of
        # providing useful output.
        self.assert_good_status(popen_object, stderr)

        # Parse the XML string. As above, we pass the stderr just in
        # case we need to error out.
        xml_root        = self.get_xml_root(stdout, stderr)

        # Lastly, we extract the date from the XML root.
        return self.pull_date_from_xml(xml_root)

    def init_popen_object (self):
        # When I run ExifTool, I want raw numbers and XML, and I want to
        # scan for XMP in case it's in there all stupid. I'll grab both
        # stdout and stderr in case there's a problem.
        return Popen(["exiftool",
                      "-n",
                      "-X",
                      "-scanForXMP",
                      self.path_to_image],
                     stdout = PIPE,
                     stderr = PIPE)

    def assert_good_status (self, popen_object, stderr):
        # If the return code is zero, then we're fine, and we don't have
        # to do anything.
        if popen_object.returncode != 0:
            # This exception also takes the error output, in case any
            # exists.
            raise ExifToolFailed(self.path_to_image, stderr)

    def get_xml_root (self, stdout, stderr):
        try:
            # Try to parse the XML.
            return ET.fromstring(stdout)

        except:
            # If we can't, exiftool must have screwed up.
            raise ExifToolFailed(self.path_to_image, stderr)

    def pull_date_from_xml (self, xml_root):
        # Be ready to check each acceptable xpath query.
        for xpath in self.date_xpaths:
            # Try to pull the date from the results of the query.
            date = self.pull_date_from_xpath(xml_root.findall(xpath))

            if date is not None:
                # If it worked, return it.
                return date

            # If we didn't get a date, we'll keep trying until we've
            # exhausted our list of xpath queries.

        # If none of the queries returned anything, we default to None.
        return None

    def pull_date_from_xpath (self, list_of_results):
        if len(list_of_results) == 0:
            # If we got no results, then there's definitely no date.
            return None

        else:
            # Otherwise, try to pull a date from the first result.
            return self.pull_date_from_elt(list_of_results[0])

    def pull_date_from_elt (self, elt):
        # Run the date regular expression on the element text.
        match   = self.re_date.match(elt.text)

        if match is None:
            # If we couldn't match it, the date is in a format we don't
            # understand.
            raise InvalidDate(elt.text)

        # Otherwise, return the formatted date.
        return self.pull_date_from_re_match(match)

    def pull_date_from_re_match (self, match):
        # We allow seconds to be an empty field.
        seconds = self.allow_empty_seconds(match)

        # We'll format according to the formatter thing, and return that
        # string.
        return self.scan_date_format(match.group("year"),
                                     match.group("month"),
                                     match.group("day"),
                                     match.group("hour"),
                                     match.group("minute"),
                                     seconds)

    def allow_empty_seconds (self, match):
        # Try to grab the "second" group.
        seconds = match.group("second")

        if seconds is None:
            # If there is none, we just set SS to 00.
            return "00"

        # Otherwise, we can return whatever we got.
        return seconds

# Functors really just act as functions.
generate_arg_parser = ArgumentParserBuilder()
pageview_dat_parser = PageviewDatParser()
pageview_validator  = PageviewFilenameValidator()
get_exif_date       = ExifDateGetter()

########################################################################
############################### Classes ################################
########################################################################

class VolumeData:
    def __init__ (self, path_to_volume):
        # Set our basic internal parameters:
        #
        #   volume:             str volume id
        #   path_to_volume:     str path to volume directory
        #   path_to_pageview:   str path to pageview.dat file
        #   path_to_meta_yml:   str path to meta.yml file
        #   path_to_first_page: str path to 00000001.tif or 00000001.jp2
        self.set_internals(path_to_volume)

        # Get data from relevant files and APIs:
        #
        #   pageview_data:      ordered (by sequence number) list of
        #                       PageviewDatParser::PageviewTuple named
        #                       quintuples, guaranteed to start at 1
        #                       with no duplicates or skips
        #   capture_date:       str capture date for meta.yml output
        self.get_existing_data()

    def write_meta_yml (self, agent, reading_order):
        # Build the full file content string.
        meta_content            = self.build_meta_yml(agent,
                                                      reading_order)

        # Then write it to the file.
        self.write_content_to_file(meta_content, self.path_to_meta_yml)

    def set_internals (self, path_to_volume):
        # The directory should be the volume id, and I don't care about
        # the path to its containing directory.
        base, self.volume       = os_path_split(path_to_volume)

        # We'll want the actual volume path still, plus a path to the
        # pageview.dat file.
        self.path_to_volume     = path_to_volume
        self.path_to_pageview   = os_path_join(path_to_volume,
                                               PAGEVIEW_DAT_FILENAME)
        self.path_to_meta_yml   = os_path_join(path_to_volume,
                                               META_YML_FILENAME)

        # We also need to find the first image in the volume.
        self.path_to_first_page = self.find_first_image()

    def get_existing_data (self):
        # Each of these deserve their own method.
        self.pageview_data      = self.get_pageview_data()
        self.capture_date       = self.get_capture_date()

    def get_pageview_data (self):
        # Get the data from the pageview file.
        data = pageview_dat_parser(self.path_to_pageview)

        # Validate that data against the volume directory.
        pageview_validator(self.path_to_volume, data)

        # If valid, return it.
        return data

    def get_capture_date (self):
        # We get the capture date from the first page image.
        return get_exif_date(self.path_to_first_page)

    def find_first_image (self):
        # Make sure our volume is formatted as expected.
        self.validate_volume_dir()

        # We're ok with tiffs and jp2s.
        tiff    = self.generate_page_filename(1, "tif")
        jp2     = self.generate_page_filename(1, "jp2")

        # Figure out which of those is real.
        return self.get_real_file_from_list(tiff, jp2)

    def validate_volume_dir (self):
        # The volume directory needs to be a directory, and the
        # pageview.dat file needs to be a file.
        self.assert_is_dir(self.path_to_volume)
        self.assert_is_file(self.path_to_pageview)

    def get_real_file_from_list (self, *paths):
        for path in paths:
            if isfile(path):
                # Return the first existing file in the list.
                return path

        # If none of those files exist, then we raise an exception.
        raise NoneAreFiles(paths)

    def assert_is_dir (self, path):
        if not isdir(path):
            # Raise an exception if this isn't a directory.
            raise NoDirectoryError(path)

    def assert_is_file (self, path):
        if not isfile(path):
            # Raise an exception if this isn't a file.
            raise NoFileError(path)

    def generate_page_filename (self, number, extension):
        # Generate the filename itself first.
        filename    = PAGE_IMAGE_FORMAT(num = number,
                                        ext = extension)

        # Our result should be a full path to the file (which should be
        # in the volume directory).
        return os_path_join(self.path_to_volume, filename)

    def build_meta_yml (self, agent, reading_order):
        # The full file is just the header concatenated with the
        # pagetags.
        return self.meta_yml_header(agent, reading_order)   \
                + self.meta_yml_pagetags()

    def meta_yml_header (self, agent, reading_order):
        # We always include the capture agent and date.
        result  = "capture_agent:  '{}'\n".format(agent)
        result += "capture_date:   '{}'\n".format(self.capture_date)

        # We may also include the reading order.
        return result + self.reading_order_if_needed(reading_order)

    def reading_order_if_needed (self, reading_order):
        if reading_order == DEFAULT_READING_ORDER:
            # Default read order means the empty string.
            return ""

        else:
            return self.meta_yml_reading_order(reading_order)

    def meta_yml_reading_order (self, reading_order):
        # We set both the scanning and the reading order.
        result  = "scanning_order: '{}'\n".format(reading_order)
        result += "reading_order:  '{}'\n".format(reading_order)

        return result

    def meta_yml_pagetags (self):
        # Start with an empty string.
        result  = ""

        for filename, sequence, page_number, confidence, page_feature \
                in self.pageview_data:
            # Add each page to the string.
            result += self.pagedata_for_row(filename,
                                            page_number,
                                            page_feature)

        # If there was any pagedata to speak of, return it.
        return self.prepend_pagedata_if_nonempty(result)

    def pagedata_for_row (self, filename, page_number, page_feature):
        if page_number == "" and page_feature == "":
            # If there's neither number nor feature, return nothing for
            # this row.
            return ""

        else:
            # Otherwise, we'll start with the filename and add whatever
            # data we have.
            return "    {}:\n{}{}".format(
                    filename,
                    self.add_line_if_nonempty("orderlabel",
                                              page_number),
                    self.add_line_if_nonempty("label",
                                              page_feature))

    def add_line_if_nonempty (self, key, value):
        if value == "":
            # If the value is empty, return an empty string.
            return ""

        else:
            # Otherwise, we return the key and value, all indented way
            # out.
            return "        {:<11} '{}'\n".format(key + ":", value)

    def prepend_pagedata_if_nonempty (self, pagedata):
        if pagedata == "":
            # If there's none, we'll just return an empty dictionary.
            return "pagedata: { }\n"

        else:
            # If there was pagedata, return it all together.
            return "pagedata:\n" + pagedata

    def write_content_to_file (self, content, path_to_file):
        # Open the file, write its contents, and close the file.
        file_object = open(path_to_file, "w")
        file_object.write(content)
        file_object.close()

########################################################################
############################# Main Routine #############################
########################################################################

class MainRoutine:
    def __call__ (self, parsed_args):
        # Set initial internals based on the arguments.
        self.set_internals(parsed_args)

        # Build the data without writing any files or anything.
        self.build_data()

        # If that went ok, all that's left is to write the files.
        self.write_files()

        echogood("Done!")

    def set_internals (self, parsed_args):
        self.agent          = parsed_args.agent
        self.reading_order  = parsed_args.reading_order
        self.volumes        = parsed_args.volumes

    def build_data (self):
        # The data will be a list for us to iterate through.
        self.data   = [ ]
        total_num   = len(self.volumes)

        for volume, i in zip(self.volumes, count(1)):
            # This reads and validates all the pageview data for each
            # volume.
            self.data.append(VolumeData(volume))

            # Let the user know.
            echogood("Finished reading {} ({:d}/{:d}) ...".format(
                self.data[-1].path_to_pageview, i, total_num))

    def write_files (self):
        echogood("Looks good! Writing files ...")

        for volume, i in zip(self.data, count()):
            # Write each file.
            volume.write_meta_yml(self.agent, self.reading_order)

if __name__ == "__main__":
    # Prep the argument parser.
    from argparse import ArgumentParser
    parser = generate_arg_parser(ArgumentParser(
                description = DETAILED_DESCRIPTION))

    # Parse the actual arguments.
    args    = parser.parse_args()

    try:
        MainRoutine()(args)

    except PageviewToMetaError as e:
        # We'll handle internal errors without a traceback.
        error_str = str(e)

        echobad("Caught {}:".format(e.__class__.__name__))
        echobad(error_str)

        raise SystemExit(1)
